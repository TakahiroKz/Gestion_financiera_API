from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.roles.service import RoleService
from src.roles.schemas import (RoleCreate, RoleResponse, RoleUpdate, RoleDelete, RoleListResponse, RoleGetByID, RoleGetByName)
from src.schemas import GenResponse
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

@role_router.post("/update", response_model=RoleResponse)
async def update_role(data: RoleUpdate, db:AsyncSession = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    try:
        updated_role = await RoleService.update_role(db,data)
        return RoleResponse(
            id = updated_role.id,
            name = updated_role.name,
            description = updated_role.description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@role_router.delete("/delete/{name}", status_code=204)
async def delete_role(name: str, db : AsyncSession = Depends(get_db)):
    try:
        await RoleService.delete_role(db, RoleDelete(name=name))
        return GenResponse(
            success=True,
            message="Eliminado con exito"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail= str(e))
    
@role_router.get("/allroles", response_model=RoleListResponse)
async def get_all_roles(db:AsyncSession = Depends(get_db)):
    try:
        _roles = await RoleService.get_all_roles(db)
        roles = [RoleResponse(
                id = role.id,
                name = role.name,
                description = role.description
            ) for role in _roles]
        return RoleListResponse(
            roles=roles
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@role_router.get("/getbyname/{name}",response_model=RoleResponse)
async def get_by_name( name:str , db:AsyncSession = Depends(get_db)):
    roles = await RoleService.get_role_by_name(db,name)
    return RoleResponse(
        id = roles.id,
        name = roles.name,
        description = roles.description
    )
    
@role_router.get("/getbyid/{role_id}", response_model=RoleResponse)
async def get_by_id(role_id: int, db:AsyncSession = Depends(get_db)):
    roles = await RoleService.get_role_by_id(db, role_id)
    return RoleResponse(
        id = roles.id,
        name = roles.name,
        description = roles.description
    )
