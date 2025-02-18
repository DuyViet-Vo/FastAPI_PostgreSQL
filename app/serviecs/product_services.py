from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.product import Product
from app.schemas.product_schemas import ProductCreate, ProductUpdate

class ProductCRUD:
    @staticmethod
    def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        return db.query(Product).offset(skip).limit(limit).all()

    @staticmethod
    def get_product(db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> Product:
        db_product = Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def update_product(
        db: Session, product_id: int, product: ProductUpdate
    ) -> Optional[Product]:
        db_product = ProductCRUD.get_product(db, product_id)
        if db_product:
            update_data = product.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_product, field, value)
            db.commit()
            db.refresh(db_product)
        return db_product

    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        db_product = ProductCRUD.get_product(db, product_id)
        if db_product:
            db.delete(db_product)
            db.commit()
            return True
        return False