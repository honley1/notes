from datetime import datetime
from typing import TYPE_CHECKING
from .base import BaseSchema, BaseModel

if TYPE_CHECKING:
    from .note import Note

class User(BaseSchema):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime
    notes: list[Note]


class UserInDB(BaseSchema):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime
    notes: list[Note]


class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
