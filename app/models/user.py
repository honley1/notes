import uuid
from datetime import datetime
from sqlalchemy import String, text
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .note import Note

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("now()"), nullable=False)

    notes: Mapped[list["Note"]] = relationship(back_populates="author", default_factory=list)