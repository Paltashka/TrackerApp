from typing import Optional
from pydantic import BaseModel
from app.features.user.models import UserRole


class CreateUser(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.USER


class ShowUser(BaseModel):
    username: str
    email: str
    role: UserRole

    class Config():
        orm_mode = True


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
