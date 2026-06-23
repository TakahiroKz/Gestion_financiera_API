from sqlalchemy.ext.asyncio import AsyncSession
from src.users.repository import UserRepository
from src.users.schemas import UserCreate, UserUpdate, UserGetByEmail, UserResponse
from src.core.paginador.paginador import PaginatedResponse
from src.core.security import hash_password
class UserService:
    async def create_user(db: AsyncSession, data:UserCreate) -> UserResponse:
        existing_user = await UserRepository(db).get_user_by_email(data.email)
        if existing_user:
            raise ValueError("El usuario ya existe")
        new_user = UserCreate(username = data.username, password = hash_password(data.password), email = data.email)
        created_user = await UserRepository(db).create_user(new_user)
        return created_user
    
    async def update_user(db:AsyncSession, data:UserUpdate):
        updated_user = await UserRepository(db).update_user(data.email, data)
        return updated_user
    
    async def delete_user(db: AsyncSession, email: str):
        deleted_user = await UserRepository(db).delete_user(email)
        return deleted_user
    
    async def get_user(db: AsyncSession, data:UserGetByEmail):
        existing_user = await UserRepository(db).get_user_by_email(data.email)
        return existing_user
    
    async def get_users(db: AsyncSession, page:int, limit: int):
        existing_user = await UserRepository(db).get_all_users(page, limit)
        return existing_user
