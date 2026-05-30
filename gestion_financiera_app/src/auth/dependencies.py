from uuid import UUID
from fastapi import Depends, HTTPException, status
from jose import JWTError
from src.core.security import decode_access_token
from src.users.models import User
from src.users.repository import UserRepository
from src.core.database import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from collections.abc import Callable
from src.core.database import get_db

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                     detail = "No se logro validar las credenciales",
                                     headers={"WWW-Authenticate":"Bearer"})
async def get_current_user(
        session: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception
        user_id : str | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    user = await UserRepository(session).get_user_by_id(UUID(user_id))
    return user

async def get_current_active_user(
        current_user: User = Depends(get_current_user)       
)-> User:
    
    if not current_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Inactive user"
        )
    return current_user

def require_role(*allowed_roles: str):
    async def role_checker(
            current_user: User = Depends(get_current_active_user),
    )-> User:
        user_role = current_user.role.name
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )
        
        return current_user
    
    return role_checker