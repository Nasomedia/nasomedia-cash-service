from typing import List, Optional

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from app.core.config import Settings

from app.crud.base import CRUDBase
from app.models import CashDeposit
from app.schemas import CashDepositUpdate, CashDepositCreate

class CRUDCashDeposit(CRUDBase[CashDeposit, CashDepositUpdate, CashDepositCreate]):
    def get_with_payment_key(
        self, db: Session, *, payment_key: str
    ) -> CashDeposit:
        return db.query(self.model)\
            .filter(self.model.payment_key==payment_key)\
            .first()
    
    def get_with_consumer(
        self, 
        db: Session,
        *, 
        consumer_id: int,
        skip: int,
        limit: int
    ) -> List[CashDeposit]:
        return db.query(self.model)\
            .filter(self.model.consumer_id==consumer_id)\
            .offset(skip).limit(limit)\
            .all()

    def create_with_consumer(
        self, db: Session, *, obj_in: CashDepositCreate, consumer_id: str
    ) -> CashDeposit:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, consumer_id=consumer_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

cash_deposit = CRUDCashDeposit(CashDeposit)