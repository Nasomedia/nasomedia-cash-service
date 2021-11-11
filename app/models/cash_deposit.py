from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .consumer import Consumer
from .consumer import Consumer

class CashDeposit(Base):
    __tablename__ = "cash_deposit"
    id = Column(Integer, primary_key=True, index=True)

    description = Column(String, nullable=True)
    deposit_amount = Column(Integer, nullable=False)

    request_at = Column(DateTime(timezone=True), nullable=True)
    ack_at = Column(DateTime(timezone=True), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)

    is_cancel = Column(Boolean, nullable=True)
    payment_key = Column(String, nullable=True)

    consumer_id = Column(Integer, ForeignKey(
        "consumer.id", ondelete="CASCADE"), nullable=True)
    consumer = relationship(Consumer)