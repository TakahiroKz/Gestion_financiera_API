from sqlalchemy.ext.asyncio import AsyncSession
from src.users.repository import UserRepository
from src.core.security import (verify_password, create_access_token, hash_password)
from src.users.schemas import UserCreate

class AuthService:
    @staticmethod
    async def register(db:AsyncSession, username: str, email: str, password: str):
        existing_user = await UserRepository(db).get_user_by_email( email)
        if existing_user:
            raise ValueError("Usuario ya registrado")
        data = UserCreate(username=username, email=email, password=hash_password(password))
        new_user = await UserRepository(db).create_user(data)
        return new_user

    @staticmethod
    async def login(db: AsyncSession, email: str, password: str):
        user = await UserRepository(db).get_user_by_email(email)
        if not user:
            raise ValueError("Credenciales invalidas")
        if not verify_password(password, user.hashed_password):
            raise ValueError("Credenciales invalidas")
        
        token = create_access_token(subject=user.id)
        return token