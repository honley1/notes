import os
from typing import AsyncGenerator
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import text
from datetime import datetime

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("DATABASE_URL")


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=text("now()"), nullable=False);
    updated_at: Mapped[datetime] = mapped_column(server_default=text("now()"), nullable=False);


engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session