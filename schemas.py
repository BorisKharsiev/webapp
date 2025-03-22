from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models import TaskStatus

class TaskBase(BaseModel):
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 0

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None