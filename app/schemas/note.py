from datetime import datetime
from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class Note(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    author: User


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    title: str
    content: str