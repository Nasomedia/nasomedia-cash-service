from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session


from app import crud, schemas, models, deps

router = APIRouter()


@router.get("", response_model=List[schemas.CashUsage])
def read_cash_usages(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_user),
    *,
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve cash usages
    """
    if user.is_superuser:
        cash_usages = crud.cash_deposit.get_multi(db, skip=skip, limit=limit)
    else:
        cash_usages = crud.cash_usage.get_multi_with_consumer(
            db,
            consumer_id=user.id,
            skip=skip, 
            limit=limit
        )
    return cash_usages


@router.post("", response_model=schemas.CashUsage)
def create_cash_usage(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_user),
    *,
    usage_in: schemas.CashUsageCreate
):
    """
    Create new cash usage
    """
    
    cash_usage = crud.cash_usage.create_with_consumer(db, obj_in=usage_in, consumer_id=user.id)
    return cash_usage


@router.put("/{usage_id}", response_model=schemas.CashUsage)
def update_cash_usage(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_superuser),
    *,
    usage_id: int,
    usage_in: schemas.CashUsageUpdate
):
    """
    Update cash usage
    """
    cash_usage = crud.cash_usage.get(db, id=usage_id)
    if not cash_usage:
        raise HTTPException(status_code=404, detail="Tag not found")
    cash_usage = crud.cash_usage.update(db, db_obj=cash_usage, obj_in=usage_in)
    return cash_usage


@router.delete("/{usage_id}", response_model=schemas.CashUsage)
def delete_cash_usage(
    db: Session = Depends(deps.get_db),
    user: schemas.User = Depends(deps.get_current_active_user),
    *,
    usage_id: int,
):
    "Delete cash usage"
    cash_usage = crud.cash_usage.get(db, id=usage_id)
    if not cash_usage:
        raise HTTPException(status_code=404, detail="Cash usage not found")
    cash_usage = crud.cash_usage.delete(db, id=usage_id)
    return cash_usage
