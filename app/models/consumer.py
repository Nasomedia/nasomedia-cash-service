from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db import Base

class Consumer(Base):
    __tablename__ = "test_model"
    id = Column(Integer, primary_key=True, index=True)

    cash = Column(Integer, nullable=False)