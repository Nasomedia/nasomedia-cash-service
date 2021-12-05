from typing import Optional
from pydantic import BaseModel

# Shared properties
class PublisherBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    # profile_url: Optional[str] = None
    # profile_image: Optional[str] = None

# Properties to receive on creation
class PublisherCreate(PublisherBase):
    name: str

# Properties to receive on update
class PublisherUpdate(PublisherBase):
    pass

# Properties shared by models stored in DB
class PublisherInDBBase(PublisherBase):
    id: int
    
    name: str
    description: str
    # profile_url: str

    class Config:
        orm_mode = True

# Properties to return to client
class Publisher(PublisherInDBBase):
    pass

# Properties properties stored in DB
class PublisherInDB(PublisherInDBBase):
    pass