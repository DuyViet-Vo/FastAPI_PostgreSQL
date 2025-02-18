from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schemas import UserCreate
from app.core.security import get_password_hash, verify_password

class UserCRUD:
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = UserCRUD.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user