from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.crud.utils import get_kst_now
from app.db import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .consumer import Consumer
from .consumer import Consumer

import uuid

class CashDeposit(Base):
    __tablename__ = "cash_deposit"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    description = Column(String, nullable=True)
    deposit_amount = Column(Integer, nullable=False)
    secret = Column(String, nullable=True)

    requested_at = Column(DateTime(timezone=True), nullable=False, default=get_kst_now)
    ack_at = Column(DateTime(timezone=True), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)

    is_canceled = Column(Boolean, nullable=False, default=False)
    payment_key = Column(String, nullable=True)

    consumer_id = Column(Integer, ForeignKey(
        "consumer.id", ondelete="CASCADE"), nullable=False)
    consumer = relationship(Consumer)