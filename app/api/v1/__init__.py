from fastapi import APIRouter

from app.api.v1.endpoints import consumer
from app.api.v1.endpoints import usage
from app.api.v1.endpoints import deposit
from app.api.v1.endpoints import purchase

api_router = APIRouter()
api_router.include_router(consumer.router, prefix="/cash/consumers", tags=["consumer"])
api_router.include_router(usage.router, prefix="/cash/usages", tags=["usage"])
api_router.include_router(deposit.router, prefix="/cash/deposits", tags=["deposit"])
api_router.include_router(purchase.router, prefix="/cash/purchase", tags=["purchase"])