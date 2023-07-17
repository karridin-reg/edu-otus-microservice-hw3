from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    phone: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
