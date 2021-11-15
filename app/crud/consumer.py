from typing import List, Optional
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Consumer
from app.schemas import ConsumerCreate, ConsumerUpdate

class CRUDConsumer(CRUDBase[Consumer, ConsumerCreate, ConsumerUpdate]):
    def create_with_user(
        self, 
        db: Session,
        *,
        obj_in: ConsumerCreate, 
        user_id: int
    ):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

consumer = CRUDConsumer(Consumer)