from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.config import settings
from app.serviecs.user_services import UserCRUD
from app.schemas.user_schemas import UserCreate, Token, UserInDB, UserLogin
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=UserInDB)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Kiểm tra email đã tồn tại
    db_user = UserCRUD.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã được đăng ký"
        )
    
    # Kiểm tra username đã tồn tại
    db_user = UserCRUD.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username đã được sử dụng"
        )
    
    return UserCRUD.create_user(db, user)

@router.post("/login", response_model=Token)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    user = UserCRUD.authenticate_user(db, user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}