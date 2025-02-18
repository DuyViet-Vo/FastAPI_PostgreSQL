from typing import Generator, Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User
from app.serviecs.user_services import UserCRUD

# Sử dụng APIKeyHeader thay vì OAuth2PasswordBearer
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Security(api_key_header),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    try:
        # Loại bỏ prefix "Bearer " nếu có
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")

        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = UserCRUD.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user
