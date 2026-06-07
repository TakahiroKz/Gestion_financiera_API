from pydantic import BaseModel, Field, ConfigDict

class RoleCreate(BaseModel):
    name: str = Field(min_length=2)
    description: str | None = None

class RoleUpdate(BaseModel):
    name: str | None = Field(min_length=2, default=None)
    description: str | None = None

class RoleDelete(BaseModel):
    name: str

class RoleGetByName(BaseModel):
    name:str

class RoleGetByID(BaseModel):
    id: int

class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)

class RoleListResponse(BaseModel):
    roles: list[RoleResponse]