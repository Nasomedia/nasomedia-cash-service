from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .consumer import Consumer
from .consumer import Consumer

class CashUsage(Base):
    __tablename__ = "cash_usage"
    id = Column(Integer, primary_key=True, index=True)

    description = Column(String, nullable=False)
    usage_amount = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False)

    consumer_id = Column(Integer, ForeignKey(
        "consumer.id", ondelete="CASCADE"), nullable=True)
    consumer = relationship(Consumer)