from typing import Optional
from pydantic import BaseModel

# Shared properties
class GenreBase(BaseModel):
    name: Optional[str] = None

# Properties to receive on creation
class GenreCreate(GenreBase):
    name: str

# Properties to receive on update
class GenreUpdate(GenreBase):
    pass

# Properties shared by models stored in DB
class GenreInDBBase(GenreBase):
    id: int
    
    name: str

    class Config:
        orm_mode = True

# Properties to return to client
class Genre(GenreInDBBase):
    pass

# Properties properties stored in DB
class GenreInDB(GenreInDBBase):
    pass