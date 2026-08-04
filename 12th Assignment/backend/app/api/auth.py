from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from app.services.auth_service import AuthService, get_current_user
from app.utils.security import create_access_token
from app.database.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    return await AuthService.register_user(db, user_data)

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    login_data = UserLogin(username=form_data.username, password=form_data.password)
    user = await AuthService.authenticate_user(db, login_data)
    token = create_access_token(data={"sub": user.id, "username": user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
