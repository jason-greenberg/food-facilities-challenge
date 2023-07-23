from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    is_active: bool = True

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

class User(UserBase):
    id: int
    hashed_password: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
