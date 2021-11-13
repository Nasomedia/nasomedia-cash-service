from fastapi import APIRouter

from app.api.v1.endpoints import consumer
from app.api.v1.endpoints import cash_usage
from app.api.v1.endpoints import cash_deposit

api_router = APIRouter()
api_router.include_router(consumer.router, prefix="/consumers", tags=["consumer"])
api_router.include_router(cash_usage.router, prefix="/cash/usages", tags=["cash"])
api_router.include_router(cash_deposit.router, prefix="/cash/deposits", tags=["cash"])