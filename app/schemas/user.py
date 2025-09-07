from datetime import datetime
from .base import BaseSchema, BaseModel


class UserResponse(BaseSchema):
    id: str
    username: str
    created_at: datetime
    updated_at: datetime


class UserRequest(BaseModel):
    username: str
    password: str
