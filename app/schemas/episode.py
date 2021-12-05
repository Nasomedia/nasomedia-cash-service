from fastapi import UploadFile, Form, File
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

# Shared properties
class EpisodeBase(BaseModel):
    title: Optional[str] = None
    order: Optional[int] = 0
    thumbnail_url: Optional[str] = "/na.png"
    is_book: Optional[bool] = False
    book_id: Optional[int] = 0
    price: Optional[int] = 0
    series_id: Optional[int] = 0

# Properties to receive on creation
class EpisodeCreate(EpisodeBase):
    title: str
    order: int
    thumbnail_image: UploadFile
    is_book: bool
    book_id: int
    price: int
    series_id: int

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        order: int = Form(...),
        thumbnail_image: UploadFile = File(...),
        is_book: bool = Form(...),
        series_id: int = Form(...),
        book_id: int = Form(0),
        price: int = Form(0)
    ):
        return cls(title=title,
                order=order,
                thumbnail_image=thumbnail_image,
                is_book=is_book,
                series_id=series_id,
                book_id=book_id,
                price=price)

# Properties to receive on update
class EpisodeUpdate(EpisodeBase):
    thumbnail_image: Optional[UploadFile]

    @classmethod
    def as_form(
        cls,
        title: str = Form(None),
        order: int = Form(None),
        thumbnail_image: UploadFile = File(None),
        book_id: int = Form(None),
        price: int = Form(None)
    ):
        episode_update = cls(title=title,
                order=order,
                thumbnail_image=thumbnail_image,
                book_id=book_id,
                price=price)
        print(title)
         # 값이 None인 모든 속성 삭제
        attrs =  list(episode_update.__dict__.items())
        for attr, value in attrs:
            if value is None:
                delattr(episode_update, attr)
        return episode_update

# Properties shared by models stored in DB
class EpisodeInDBBase(EpisodeBase):
    id: int
    
    title: str
    order: int
    thumbnail_url: str
    is_book: bool
    book_id: int
    price: int

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Properties to return to client
class Episode(EpisodeInDBBase):
    pass

# Properties properties stored in DB
class EpisodeInDB(EpisodeInDBBase):
    series_id: int