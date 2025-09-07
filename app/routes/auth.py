from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserInDB, UserRequest
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user

from app.utils.hash import get_password_hash, verify_password
from app.utils.jwt import create_access_token

router = APIRouter()

@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.username == user_data.username))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken"
            )
        
        username = user_data.username
        password_hash = get_password_hash(user_data.password)

        user = User(
            username=username,
            password=password_hash
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        user_in_db = UserInDB.model_validate(user)
        access_token = create_access_token({"id": user_in_db.id, "username": user_in_db.username})

        return {
            "message": "User registered successfully",
            "data": {
                "user": user_in_db.model_dump(),
                "token": access_token
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.username == user_data.username))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        user_in_db = UserInDB.model_validate(user)
        access_token = create_access_token({"id": user_in_db.id, "username": user_in_db.username})

        return {
            "message": "Login successful",
            "data": {
                "user": user_in_db.model_dump(),
                "token": access_token
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    try:
        user_data = UserInDB.model_validate(user)
        return {
            "message": "User profile retrieved successfully",
            "data": user_data.model_dump()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )