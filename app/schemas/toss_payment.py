from datetime import datetime
from typing import Any, Optional
from enum import Enum

from pydantic import BaseModel, HttpUrl


class CardCompany(str, Enum):
    shinhan = '신한'
    hyundai = '현대'
    samsung = '삼성'
    woori = '우리'
    kb = '국민'
    lotte = '롯데'
    nh = '농협'
    hana = '하나'
    bc = 'BC'
    citi = '씨티'
    kakaobank = '카카오뱅크'
    kdb = 'KDB'
    sh = '수협'
    jb = '전북'
    epostbank = '우체국'
    kfcc = '새마을'
    sb = '저축'
    jeju = '제주'
    gwangju = '광주'
    shinhyup = '신협'
    jcb = 'JCB'
    unionpay = '유니온페이'
    master = '마스터'
    visa = '비자'
    diners_club = '다이너스'
    discover = '디스커버'


class CardInfo(BaseModel):
    company: CardCompany
    number: str
    installmentPlanMonths: int
    approveNo: str
    useCardPoint: bool
    cardType: str
    ownerType: str
    receiptUrl: HttpUrl
    acquireStatus: str
    isInterestFree: bool


class VirtualAccountInfo(BaseModel):
    accountNumber: str
    bank: str
    customerName: str
    dueDate: datetime


class PaymentBase(BaseModel):
    secret: str
    status: str
    orderId: str


class Payment(PaymentBase):
    paymentKey: str
    mId: str
    currency: str
    method: str
    totalAmount: int
    balanceAmount: int
    requestedAt: datetime
    approvedAt: Optional[datetime]
    useDiscount: bool
    discount: Any
    useEscrow: bool
    useCashReceipt: bool
    card: Optional[CardInfo]
    virtualAccount: Optional[VirtualAccountInfo]
    cashReceipt: Any
    cancels: Any
    secret: Optional[str]

class RefundReceiveAccount():
    bank: str
    account_number: str
    holder_name: str
