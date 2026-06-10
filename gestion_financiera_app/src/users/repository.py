
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from math import ceil

from src.users.models import User
from src.users.schemas import UserCreate, UserUpdate, UserResponse
from src.core.paginador.paginador import PaginatedResponse

class UserRepository:
    def __init__ (self, db: AsyncSession):
        self.db = db

    async def create_user(self, data: UserCreate) -> User:
        try:
            new_user = User(
                username = data.username,
                email = data.email,
                hashed_password = data.password,
                role_id = 2
            )
            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)
            return new_user
        except Exception as e:
            await self.db.rollback()
            return e
    
    async def get_user_by_id(self, user_id:int) -> User | None:
        try:
            stmt = select(User).options(selectinload(User.role)).where(User.id == user_id)
            result = await self.db.execute(stmt)
            return result.scalars().one_or_none()
        except Exception as e:
            return e
    
    async def get_user_by_email(self, email:str) -> User | None:
        try:
            stmt = select(User).options(selectinload(User.role)).where(User.email == email)
            result = await self.db.execute(stmt)
            return result.scalars().one_or_none()
        except Exception as e:
            return e
    
    async def get_all_users(self,page:int, limit:int) -> PaginatedResponse[UserResponse]:
        offset = (page-1)* limit
        try:
            count_query = (select(func.count()).select_from(User))
            count_result = await self.db.execute(count_query)
            total = count_result.scalar()
            pages = ceil(total/limit)
            stmt = (select(User).offset(offset).limit(limit).options(selectinload(User.role)))
            result = await self.db.execute(stmt)
            result = result.scalars().all()
            users = [UserResponse(
                id = user.id,
                username = user.username,
                email = user.email,
                is_active = user.is_active,
                is_verified = user.is_verified,
                role_name = user.role.name
            )
            for user in result]

            return PaginatedResponse[UserResponse](
                items = users,
                total = total,
                page = page,
                limit = limit,
                pages = pages,
                has_next = page < pages,
                has_prev = page > 1
            )
        except Exception as e:
            raise ValueError(e)

    async def update_user(self, email:str, data: UserUpdate) -> User | None:
        try: 
            existing_user = await self.get_user_by_email(email)
            if not existing_user:
                return None
            existing_user.username = data.username or existing_user.username
            existing_user.email = data.email or existing_user.email
            existing_user.hashed_password = data.password or existing_user.hashed_password
            existing_user.is_active = data.is_active if data.is_active is not None else existing_user.is_active
            existing_user.is_verified = data.is_verified if data.is_verified is not None else existing_user.is_verified
            existing_user.role_id = data.role_id or existing_user.role_id
            await self.db.commit()
            await self.db.refresh(existing_user)
            return existing_user
        except Exception as e:
            await self.db.rollback()
            raise ValueError(e)

    async def delete_user(self, user_id:int) -> bool:
        try:
            existing_user = await self.get_user_by_id(user_id)
            if not existing_user:
                return False
            await self.db.delete(existing_user)
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            return False
        
        