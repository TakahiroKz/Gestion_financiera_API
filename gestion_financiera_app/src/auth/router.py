from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.auth.service import AuthService
from src.auth.schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    TokenResponse
)

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register", response_model=RegisterResponse)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    try:
        new_user = await AuthService.register(db, data.username, data.email, data.password)
        return RegisterResponse(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@auth_router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db:AsyncSession = Depends(get_db)):
    try:
        token = await AuthService.login(db, data.email, data.password)
        return token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))