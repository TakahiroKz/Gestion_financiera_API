from sqlalchemy.ext.asyncio import AsyncSession
from src.roles.repository import RoleRepository
from src.roles.schemas import (
    RoleCreate,
    RoleUpdate,
    RoleDelete,
    RoleGetByID,
    RoleGetByName
)

class RoleService:
    async def create_role(db: AsyncSession, data: RoleCreate):
        existing_role = await RoleRepository(db).get_role_by_name(data.name)
        if existing_role:
            raise ValueError("El rol ya existe")
        new_role = await RoleRepository(db).create_role(data)
        return new_role
    
    async def update_role(db:AsyncSession, data:RoleUpdate):
        existing_role = await RoleRepository(db).get_role_by_name(data.name)
        if not existing_role:
            raise ValueError("El rol no existe")
        role_updated = await RoleRepository(db).update_role(data)
        return role_updated

    async def delete_role(db:AsyncSession, data:RoleDelete):
        deleted_role = await RoleRepository(db).delete_role(data)
        return deleted_role

    async def get_all_roles(db: AsyncSession):
        return await RoleRepository(db).get_all_roles()
    
    async def get_role_by_name(db:AsyncSession, name:str):
        return await RoleRepository(db).get_role_by_name(name)
    
    async def get_role_by_id(db:AsyncSession, role_id:int):
        return await RoleRepository(db).get_role_by_id(role_id)
