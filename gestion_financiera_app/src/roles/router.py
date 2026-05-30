from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.roles.service import RoleService
from src.roles.schemas import (RoleCreate, RoleResponse)
from src.auth.dependencies import get_current_user, require_role
from src.users.models import User

role_router = APIRouter(prefix="/roles", tags=["Roles"])

@role_router.post("/create", response_model=RoleResponse)
async def create_role(data: RoleCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    try:
        new_role = await RoleService.create_role(db,data)
        return RoleResponse(
            id = new_role.id,
            name = new_role.name,
            description = new_role.description
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))