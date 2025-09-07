from datetime import datetime
from typing import TYPE_CHECKING

from .base import BaseSchema, BaseModel

if TYPE_CHECKING:
    from .user import User


class Note(BaseSchema):
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    author: "User"


class NoteInDB(BaseSchema):
    id: str
    title: str
    content: str
    author_id: str
    created_at: datetime
    updated_at: datetime


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
