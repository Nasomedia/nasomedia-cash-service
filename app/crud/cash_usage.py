from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import CashUsage
from app.schemas import CashUsageCreate, CashUsageUpdate

class CRUDCashUsage(CRUDBase[CashUsage, CashUsageCreate, CashUsageUpdate]):
    def get_with_consumer(
        self, 
        db: Session,
        *, 
        consumer_id: int,
        skip: int,
        limit: int
    ) -> List[CashUsage]:
        return db.query(self.model)\
            .filter(self.model.consumer_id==consumer_id)\
            .offset(skip).limit(limit)\
            .all()

    def create_with_consumer(
        self, db: Session, *, obj_in: CashUsageCreate, consumer_id: str
    ) -> CashUsage:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, consumer_id=consumer_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj    
cash_usage = CRUDCashUsage(CashUsage)