from typing import Optional
from pydantic import BaseModel

# Shared properties
class TagBase(BaseModel):
    name: Optional[str] = None

# Properties to receive on creation
class TagCreate(TagBase):
    name: str

# Properties to receive on update
class TagUpdate(TagBase):
    pass

# Properties shared by models stored in DB
class TagInDBBase(TagBase):
    id: int
    
    name: str

    class Config:
        orm_mode = True

# Properties to return to client
class Tag(TagInDBBase):
    pass

# Properties properties stored in DB
class TagInDB(TagInDBBase):
    pass