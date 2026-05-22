from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=2)
    email: EmailStr
    password:str = Field(min_length=6)

class UserUpdate(BaseModel):
    username: str | None = Field(min_length=2)
    email: EmailStr | None = None
    password: str | None = Field(min_length=6, default=None)
    is_active: bool | None = None
    is_verified: bool | None = None
    role_id: int | None = None

class UserDelete(BaseModel):
    id: int

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active:bool
    is_verified: bool
    role_name: str

    model_config = ConfigDict(from_attributes=True)
