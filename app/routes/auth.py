from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserInDB, UserRequest
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user

from app.utils.response import response
from app.utils.hash import get_password_hash, verify_password
from app.utils.jwt import create_access_token

router = APIRouter()

@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.username == user_data.username))
        if result.scalar_one_or_none():
            return response(False, "Username already taken", 400)
        
        username = user_data.username
        password_hash = get_password_hash(user_data.password)

        user = User(
            username=username,
            password=password_hash
        )

        db.add(user)

        await db.commit()
        await db.refresh(user)

        user = UserInDB.model_validate(user)

        access_token = create_access_token(user_data.model_dump())

        return response(True, {"token": access_token}, 201)
    except Exception as e:
        return response(False, str(e), 500)


@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.username == user_data.username))
        
        user = result.scalar_one_or_none()
        
        if not user:
            return response(False, "Invalid credentials", 401)
        

        if not verify_password(user_data.password, user.password):
            return response(False, "Invalid credentials", 401)
        
        user = UserInDB.model_validate(user)

        access_token = create_access_token(user_data.model_dump())

        return response(True, {"token": access_token}, 200)
    except Exception as e:
        return response(False, str(e), 500)


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return response(True, user.model_dump(), 200)