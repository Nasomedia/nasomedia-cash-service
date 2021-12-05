from typing import Optional
from pydantic import BaseModel

# Shared properties
class AuthorBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    # profile_url: Optional[str] = None
    # profile_image: Optional[str] = None

# Properties to receive on creation
class AuthorCreate(AuthorBase):
    name: str

# Properties to receive on update
class AuthorUpdate(AuthorBase):
    pass

# Properties shared by models stored in DB
class AuthorInDBBase(AuthorBase):
    id: int
    
    name: str
    description: str
    # profile_url: str

    class Config:
        orm_mode = True

# Properties to return to client
class Author(AuthorInDBBase):
    pass

# Properties properties stored in DB
class AuthorInDB(AuthorInDBBase):
    pass