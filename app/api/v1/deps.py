import json
from typing import Generator, Union, Mapping
from fastapi import Depends
from multidict import CIMultiDict, CIMultiDictProxy, istr
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder

from app.db.session import SessionLocal
from app.core.config import settings
from app import schemas

import aiohttp

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

resuable_oauth2 = OAuth2PasswordBearer(
    tokenUrl = settings.IDENTITY_SERVICE_BASE_URL+settings.TOKEN_URL
)

async def get_current_user(
    token: str = Depends(resuable_oauth2)
) -> schemas.User:
    headers={"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"{settings.IDENTITY_SERVICE_BASE_URL}/api/v1/users/me") as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail=await resp.text())
            user_data = await resp.json()
            user = schemas.User(**user_data)
            return user

async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user)
) -> schemas.User:
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user

async def get_current_active_superuser(
    current_user: schemas.User = Depends(get_current_user)
) -> schemas:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user



Headers = Union[Mapping[Union[str, istr], str], CIMultiDict, CIMultiDictProxy]

class TossPayment():
    def __init__(self):
        """
        Deps object for Toss Payments API
        """

        self.headers: Headers = {"Authorization": f"Basic {settings.TOSS_AUTHORIZATION}"}

    def encapsulate_payment_for_client(self, obj_in: schemas.Payment):
        obj_dict = obj_in.dict()
        obj_dict["secret"] = None
        return schemas.PaymentClient(**obj_dict)

    def read_payment(self, payment_key: str):
        r = requests.get(url=f"{BASE_URL}/v1/payments/{payment_key}", headers=self.headers)
        return r.json()

    def read_payment_by_order_id(self, order_id: Union[str, int]):
        r = requests.get(url=f"{BASE_URL}/v1/payments/orders/{order_id}", headers=self.headers)
        return r.json()

    async def ack_payment(self, cash_deposit_ack_in: schemas.CashDepositAckRequest):
        payment_key = getattr(cash_deposit_ack_in, "payment_key")
        delattr(cash_deposit_ack_in, "payment_key")
        body = jsonable_encoder(cash_deposit_ack_in)
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(
                    f"{settings.TOSS_BASE_URL}/v1/payments/{payment_key}",
                    json=body) as resp:
                if resp.status != 200:
                    raise HTTPException(status_code=resp.status, detail=await resp.text())
                payment_data = await resp.json()
                payment = schemas.Payment(**payment_data)
                return payment

    async def cancel_payment(self, cash_deposit_cancel_in: schemas.CashDepositCancel):
        payment_key = getattr(cash_deposit_cancel_in, "payment_key")
        delattr(cash_deposit_cancel_in, "payment_key")
        body = jsonable_encoder(cash_deposit_cancel_in)
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(
                    f"{settings.TOSS_BASE_URL}/v1/payments/{payment_key}/cancel",
                    json=body) as resp:
                if resp.status != 200:
                    raise HTTPException(status_code=resp.status, detail=await resp.text())
                payment_data = await resp.json()
                payment = schemas.Payment(**payment_data)
                return payment

