from datetime import datetime
from typing import TYPE_CHECKING
from .base import BaseSchema, BaseModel, BaseSchema

if TYPE_CHECKING:
    from .note import Note

class User(BaseSchema):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime
    notes: list["Note"] = []


class UserInDB(BaseSchema):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime


class UserRequest(BaseModel):
    username: str
    password: str
    