from fastapi import APIRouter
from app.api.v1.endpoints import product

router = APIRouter()
router.include_router(product.router, prefix="/products", tags=["products"])
