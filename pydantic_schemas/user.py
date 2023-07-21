from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    role: int

class UserCreate(UserBase):
    ...

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # necessary config for using an orm with pydantic
    class Config:
        orm_mode = True
