from fastapi.param_functions import Query
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from . import toss_payment

# Shared properties
class CashDepositBase(BaseModel):
    description: Optional[str]

# Properties to receive on creation
class CashDepositCreate(CashDepositBase):
    deposit_amount: int
    description: Optional[str] = None

# Properties to receive on update
class CashDepositUpdate(CashDepositBase):
    secret: Optional[str] = None

    request_at: Optional[datetime]
    ack_at: Optional[datetime]
    approved_at: Optional[datetime]
    due_date: Optional[datetime]

    is_canceled: Optional[bool] = False
    payment_key: Optional[str]


# Properties shared by models stored in DB
class CashDepositInDBBase(CashDepositBase):
    id: str

    deposit_amount: int
    secret: Optional[str] = None

    requested_at: datetime
    ack_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    due_date: Optional[datetime] = None

    is_canceled: bool = False
    payment_key: Optional[str]

    consumer_id: int

    class Config:
        orm_mode = True

# Properties to return to client
class CashDeposit(CashDepositInDBBase):
    pass

# Properties properties stored in DB
class CashDepositInDB(CashDepositInDBBase):
    pass

# Properties to acknowledge a cash deposit
class CashDepositAckRequest(CashDepositBase):
    payment_key: str
    order_id: str
    amount: int

    @classmethod
    def as_query(
        cls,
        payment_key: str = Query(...),
        order_id: str = Query(...),
        amount: int = Query(...)
    ):
        return cls(payment_key=payment_key, order_id=order_id, amount=amount)

class CashDepositAck(CashDepositBase):
    cash_deposit: CashDeposit
    payment: toss_payment.Payment

# Properties to cancel a cash deposit
class CashDepositCancelRequest(CashDepositBase):
    payment_key : str
    cancel_reason: str
    refund_receive_account: Optional[toss_payment.RefundReceiveAccount]

class CashDepositCancel(CashDepositBase):
    cash_deposit: CashDeposit
    payment: toss_payment.Payment

class CashDepositCallbackRequest(toss_payment.PaymentBase):
    pass

class CashDepositCallback(BaseModel):
    status: str
    detail: str