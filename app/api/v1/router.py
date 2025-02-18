from fastapi import APIRouter

from app.api.v1.endpoints import product, user

router = APIRouter()
router.include_router(product.router, prefix="/products", tags=["products"])
router.include_router(user.router, prefix="/auth", tags=["auth"])
