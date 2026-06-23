from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.exceptions import ResponseValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User

from src.core.database import get_db
from src.core.paginador.core import pagination_params
from src.core.paginador.paginador import PaginatedResponse
from src.users.schemas import (UserResponse, UsersResponse, UserGetByEmail, UserCreate, UserDelete,UserUpdate)
from src.users.service import UserService
from src.schemas import GenResponse

user_router = APIRouter(prefix="/user", tags=["Users"])

@user_router.get("/get_all_users", response_model=PaginatedResponse[UserResponse])
async def get_all_users(pagination = Depends(pagination_params),db: AsyncSession = Depends(get_db)):
    try:
        return await UserService.get_users(db, pagination["page"], pagination["limit"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail= str(e))

@user_router.get("/get_user_by_email", response_model=UserResponse)
async def get_user_by_email(data: UserGetByEmail ,db:AsyncSession = Depends(get_db)):
    try:
        user = await UserService.get_user(db, data)
        if user == None:
            raise HTTPException(status_code=400, detail="No se encontraron usuarios")
        return UserResponse(
            id=user.id,
            username = user.username,
            email = user.email,
            is_active = user.is_active,
            is_verified = user.is_verified,
            role_name = user.role.name
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.post("/create_user", response_model=UserResponse)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        created = await UserService.create_user(db,data)
        if created:
            raise HTTPException(status_code=400, detail="Ya se ha creado un usuario")    
        return UserResponse(
            id=created.id,
            username = created.username,
            email = created.email,
            is_active = created.is_active,
            is_verified = created.is_verified,
            role_name = created.role.name
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.put("/update_user", response_model=UserResponse)
async def update_user(data: UserUpdate, db: AsyncSession = Depends(get_db))->UserResponse:
    try:
        updated = await UserService.update_user(db, data)
        return UserResponse(
            id=updated.id,
            username = updated.username,
            email = updated.email,
            is_active = updated.is_active,
            is_verified = updated.is_verified,
            role_name = updated.role.name
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.delete("/delete_user/{email}", response_model=GenResponse)
async def delete_user(email:str, db: AsyncSession = Depends(get_db)):
    try:
        deleted = await UserService.delete_user(db, email)
        return GenResponse(
            success = deleted,
            message = "Completed"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))