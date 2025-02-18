from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.serviecs.product_services import ProductCRUD
from app.schemas.product_schemas import ProductCreate, ProductUpdate, ProductInDB
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[ProductInDB])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lấy danh sách sản phẩm"""
    products = ProductCRUD.get_products(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=ProductInDB)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lấy thông tin một sản phẩm theo ID"""
    db_product = ProductCRUD.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm"
        )
    return db_product


@router.post("/", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Tạo sản phẩm mới"""
    return ProductCRUD.create_product(db, product)


@router.put("/{product_id}", response_model=ProductInDB)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cập nhật thông tin sản phẩm"""
    db_product = ProductCRUD.update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm"
        )
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Xóa sản phẩm"""
    deleted = ProductCRUD.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm"
        )
