import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=2)
    email: EmailStr
    password:str = Field(min_length=6, max_length=64)

class UserUpdate(BaseModel):
    username: str | None = Field(min_length=2)
    email: EmailStr | None = None
    password: str | None = Field(min_length=6, max_length=64, default=None)
    is_active: bool | None = None
    is_verified: bool | None = None
    role_id: int | None = None

class UserGetByEmail(BaseModel):
    email: EmailStr

class UserDelete(BaseModel):
    email: EmailStr

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active:bool
    is_verified: bool
    role_name: str

    model_config = ConfigDict(from_attributes=True)

class UsersResponse(BaseModel):
    users : list[UserResponse]
