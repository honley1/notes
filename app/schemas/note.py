from __future__ import annotations
from datetime import datetime
from .base import BaseSchema, BaseModel
from .user import UserResponse


class NoteResponse(BaseSchema):
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    author: UserResponse


class Note(BaseSchema):
    id: str
    title: str
    content: str
    author_id: str
    created_at: datetime
    updated_at: datetime


class NoteRequest(BaseModel):
    title: str
    content: str
