import uuid
from sqlalchemy import String, text, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.dependencies.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)

    author: Mapped["User"] = relationship(back_populates="notes")
