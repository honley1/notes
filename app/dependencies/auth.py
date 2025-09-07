from sqlalchemy.sql import select
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.utils.jwt import verify_token

from app.utils import response
from app.dependencies.database import get_db

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = verify_token(credentials.credentials)
        if not payload:
            raise response(False, "Invalid credentials", 401)
        
        user_id = payload.get("id")
        if not user_id:
            raise response(False, "Invalid credentials", 401)
        
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise response(False, "Invalid credentials", 401)
        
        return user
    except Exception as e:
        raise response(False, str(e), 401)