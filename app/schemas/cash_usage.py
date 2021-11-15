from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class CashUsageBase(BaseModel):
    description: Optional[str]
    usage_amount: Optional[int]

# Properties to receive on creation
class CashUsageCreate(CashUsageBase):
    usage_amount: int

# Properties to receive on update
class CashUsageUpdate(CashUsageBase):
    pass

# Properties shared by models stored in DB
class CashUsageInDBBase(CashUsageBase):
    id: int

    usage_amount: int
    created_at: datetime

    consumer_id: int

    class Config:
        orm_mode = True

# Properties to return to client
class CashUsage(CashUsageInDBBase):
    pass

# Properties properties stored in DB
class CashUsageInDB(CashUsageInDBBase):
    pass