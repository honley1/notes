from datetime import datetime
from typing import TYPE_CHECKING
from .base import BaseSchema, BaseModel

if TYPE_CHECKING:
    from .note import Note

class User(BaseSchema):
    id: str
    username: str
    created_at: datetime
    updated_at: datetime
    notes: list["Note"] = []


class UserInDB(BaseSchema):
    id: str
    username: str
    created_at: datetime
    updated_at: datetime


class UserRequest(BaseModel):
    username: str
    password: str
