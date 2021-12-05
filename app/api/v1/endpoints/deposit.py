from typing import Any, List, Optional, Union
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.utils import get_kst_now
from app.api.v1 import deps
from app.models import cash_deposit, consumer
from app.schemas.toss_payment import Payment

from app.core.config import settings

router = APIRouter()


@router.get("", response_model=List[schemas.CashDeposit])
def read_cash_deposits(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_user),
    *,
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve cash deposits
    """
    if user.is_superuser:
        cash_deposits = crud.cash_deposit.get_multi(db, skip=skip, limit=limit)
    else:
        cash_deposits = crud.cash_deposit.get_multi_with_consumer(
            db, 
            consumer_id=user.id, 
            skip=skip, 
            limit=limit
        )
    return cash_deposits


@router.post("", response_model=schemas.CashDeposit)
def create_cash_deposit(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_user),
    *,
    deposit_in: schemas.CashDepositCreate
):
    """
    Create new cash deposit
    """

    if deposit_in.deposit_amount < 1000 or deposit_in.deposit_amount % 1000 != 0:
        raise HTTPException(status_code=400, detail="Invalid amount value")

    cash_deposit = crud.cash_deposit.create_with_consumer(db, obj_in=deposit_in, consumer_id=user.id)
    return cash_deposit


@router.post("/ack", response_model=schemas.CashDepositAck)
async def ack_cash_deposit(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    toss: deps.TossPayment = Depends(deps.TossPayment),
    deposit_ack_in: schemas.CashDepositAckRequest =  Depends(schemas.CashDepositAckRequest.as_query)
):
    """
    Acknowledge cash deposit
    """
    cash_deposit = crud.cash_deposit.get(db, id=deposit_ack_in.order_id)
    if not cash_deposit:
        raise HTTPException(status_code=404, detail="Cash deposit not found")
    if cash_deposit.payment_key:
        raise HTTPException(status_code=400, detail="Already processed payment")
    if cash_deposit.consumer_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permission")
    if deposit_ack_in.amount != cash_deposit.deposit_amount:
        raise HTTPException(status_code=400, detail="Amount value doesn't coincide")
    
    payment: schemas.Payment = await toss.ack_payment(deposit_ack_in)
    if payment.status != "DONE":
        raise HTTPException(status_code=400, detail="Failed to acknowledge payment")    

    if payment.approvedAt:
        consumer = cash_deposit.consumer
        crud.consumer.update(db, db_obj=consumer, obj_in=schemas.ConsumerUpdate(
            amount=consumer.cash+cash_deposit.deposit_amount
        ))
        cash_deposit_in = schemas.CashDepositUpdate(
            patment_key=payment.paymentKey,
            ack_at=payment.approvedAt,
            approved_at=payment.approvedAt
        )
    else:
        cash_deposit_in = schemas.CashDepositUpdate(
            payment_key=payment.paymentKey,
            ack_at=get_kst_now(),
            due_date=payment.virtualAccount.dueDate,
            secret=payment.secret
        )

    cash_deposit = crud.cash_deposit.update(
        db, db_obj=cash_deposit, obj_in=cash_deposit_in
    )
    payment.secret = None
    response = schemas.CashDepositAck(cash_deposit=cash_deposit, payment=payment)

    return response


@router.post("/callback", response_model=schemas.CashDepositCallback)
def cash_deposit_callback(
    db: Session = Depends(deps.get_db),
    *,
    deposit_callback_in: schemas.CashDepositCallbackRequest
):
    "Cash deposit complete or cancel callback"
    cash_deposit =  crud.cash_deposit.get(db, id=deposit_callback_in.orderId)
    if not cash_deposit:
        raise HTTPException(status_code=404, detail=f"OrderId: {deposit_callback_in.orderId} not found")
    if cash_deposit.secret != deposit_callback_in.secret:
        raise HTTPException(status_code=400, detail="Invalid secret, please check your secret")

    if deposit_callback_in.status == "DONE":
        cash_deposit = crud.cash_deposit.update(db, db_obj=cash_deposit, obj_in=schemas.CashDepositUpdate(
            approved_at=get_kst_now()
        ))
        consumer = cash_deposit.consumer
        crud.consumer.update(db, db_obj=consumer, obj_in=schemas.ConsumerUpdate(
            amount=consumer.cash+cash_deposit.deposit_amount
        ))
        detail = "Successfully update deposit"
    else:
        cash_deposit = crud.cash_deposit.update(
            db, db_obj=cash_deposit, obj_in=schemas.CashDepositUpdate(is_canceled=True))
        detail = "Successfully cancel deposit"
    response = schemas.CashDepositCallback(status=deposit_callback_in.status, detail=detail)
    return response


@router.post("/cancel", response_model=schemas.CashDepositCancel)
async def cancel_cash_deposit(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_user),
    toss: deps.TossPayment = Depends(deps.TossPayment),
    *,
    deposit_cancel_in: schemas.CashDepositCancelRequest
):
    "Cancel cash deposit"

    cash_deposit = crud.cash_deposit.get_with_payment_key(db, payment_key=deposit_cancel_in.payment_key)
    if not cash_deposit:
        raise HTTPException(status_code=400, detail="Invalid payment key")
    if cash_deposit.consumer_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permission")
    if cash_deposit.deposit_amount > cash_deposit.consumer.cash:
        raise HTTPException(status_code=400, detail="Not enough cash to refund")
    if get_kst_now() - cash_deposit.approved_at > timedelta(days=3):
        raise HTTPException(status_code=400, detail="The cancellation date has passed, It is 3 days after purchasing")

    payment: schemas.Payment = await toss.cancel_payment(deposit_cancel_in)
    if payment.status != "PARTIAL_CANCELED" or payment.status != "CANCELED":
        raise HTTPException(status_code=400, detail="Failed to cancel payment")

    consumer = cash_deposit.consumer
    crud.consumer.update(db, db_obj=consumer, obj_in=schemas.ConsumerUpdate(
        amount=consumer.cash-cash_deposit.deposit_amount
    ))
    
    cash_deposit = crud.cash_deposit.update(
        db, db_obj=cash_deposit, obj_in=schemas.CashDepositUpdate(is_canceled=True))
    payment.secret = None
    response = schemas.CashDepositCancel(cash_deposit=cash_deposit, payment=payment)

    return response


@router.delete("/{deposit_id}", response_model=schemas.CashDeposit)
def delete_cash_deposit(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_user),
    *,
    deposit_id: int,
):
    "Delete cash deposit"
    cash_deposit = crud.cash_deposit.get(db, id=deposit_id)
    if not cash_deposit:
        raise HTTPException(status_code=404, detail="Cash deposit not found")
    if cash_deposit.consumer_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permission")
    cash_deposit = crud.cash_deposit.delete(db, id=deposit_id)
    return cash_deposit
