from datetime import datetime
from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .note import Note

class User(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime
    notes: list[Note]

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: str
    password: str