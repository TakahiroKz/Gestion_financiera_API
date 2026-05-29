
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User
from src.users.schemas import UserCreate, UserUpdate

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
    
    async def get_get_all_users(self) -> list[User]:
        try:
            stmt = select(User)
            result = await self.db.execute(stmt)
            return list(result.scalars().all())
        except Exception as e:
            return e

    async def update_user(self, user_id:int, data: UserUpdate) -> User | None:
        try: 
            existing_user = await self.get_user_by_id(user_id)
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
            return e

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
            return e
        
        