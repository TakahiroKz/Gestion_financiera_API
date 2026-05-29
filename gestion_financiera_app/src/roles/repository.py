from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.roles.models import Role
from src.roles.schemas import RoleCreate, RoleUpdate

class RoleRepository:
    def __init__(self,db: AsyncSession):
        self.db = db

    async def create_role(self, data: RoleCreate) -> Role:
        try:
            new_role = Role(
                name = data.name,
                description = data.description
            )
            self.db.add(new_role)
            await self.db.commit()
            await self.db.refresh(new_role)
            return new_role
        except Exception as e:
            await self.db.rollback()
            return e
        
    async def get_role_by_id(self,  role_id:int) -> Role | None:
        try:
            stmt = (select(Role).where(Role.id==role_id))
            result = await self.db.execute(stmt)
            return result.scalars().one_or_none()
        except Exception as e:
            return e
        
    async def get_all_roles(self) -> list[Role]:
        try:
            stmt = select(Role)
            result = await self.db.execute(stmt)
            return list(result.scalars().all())
        except Exception as e: 
            return e

    async def get_role_by_name(self, name:str) -> Role | None:
        try:
            stmt = (select(Role).where(Role.name==name))
            result = await self.db.execute(stmt)
            return result.scalars().one_or_none()
        except Exception as e:
            return e
        
    async def update_role(self, role_id:int, data: RoleUpdate) -> Role | None:
        try:
            existing_role = await self.db.execute(select(Role).where(Role.id == role_id))
            if not existing_role:
                return None
            existing_role.name = data.name or existing_role.name
            existing_role.description = data.description or existing_role.description
            await self.db.commit()
            await self.db.refresh(existing_role)
            return existing_role
        except Exception as e:
            await self.db.rollback()
            return e

    async def delete_role(self, role_id:int) -> bool:
        try:
            existing_role = await self.db.execute(select(Role).where(Role.id == role_id))
            if not existing_role:
                return False
            await self.db.delete(existing_role)
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            return e
