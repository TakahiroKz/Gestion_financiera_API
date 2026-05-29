from sqlalchemy.ext.asyncio import AsyncSession
from src.roles.repository import RoleRepository
from src.roles.schemas import (
    RoleCreate,
    RoleUpdate
)

class RoleService:
    async def create_role(db: AsyncSession, data: RoleCreate):
        existing_role = await RoleRepository(db).get_role_by_name(data.name)
        if existing_role:
            raise ValueError("El rol ya existe")
        new_role = await RoleRepository(db).create_role(data)
        return new_role