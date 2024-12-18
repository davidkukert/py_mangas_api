import uuid
from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None


class UserPublic(BaseModel):
    id: uuid.UUID
    username: str
    created_at: datetime
    updated_at: datetime


class UserDetails(BaseModel):
    user: UserPublic


class UserList(BaseModel):
    users: list[UserPublic]
