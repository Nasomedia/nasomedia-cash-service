from typing import Union, Mapping
from multidict import CIMultiDict, CIMultiDictProxy, istr
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from app.db.session import SessionLocal
from app.core.config import settings
from app import schemas

import aiohttp
import requests

Headers = Union[Mapping[Union[str, istr], str], CIMultiDict, CIMultiDictProxy]
BASE_URL = 'https://api.tosspayments.com'


class TossPayment():
    def __init__(self):
        """
        Deps object for Toss Payments API
        """

        self.headers: Headers = {"Authorization": f"Basic {settings.TOSS_AUTHORIZATION}"}

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

    async def cancel_payment(self, cash_deposit_cancel_in: schemas.CashDepositCancelRequest):
        body = {
            "cancelReason": cash_deposit_cancel_in.cancel_reason,
            "refundReceiveAccount": getattr(cash_deposit_cancel_in, "refund_receive_account")
        }
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(
                    f"{settings.TOSS_BASE_URL}/v1/payments/{cash_deposit_cancel_in.payment_key}/cancel",
                    json=body) as resp:
                if resp.status != 200:
                    raise HTTPException(status_code=resp.status, detail=await resp.text())
                payment_data = await resp.json()
                payment = schemas.Payment(**payment_data)
                return payment

