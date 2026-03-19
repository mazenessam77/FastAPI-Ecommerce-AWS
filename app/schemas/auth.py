from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from app.schemas.carts import CartBase


# Base
class BaseConfig:
    from_attributes = True


class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    password: str
    role: str
    is_active: bool
    created_at: datetime
    carts: List[CartBase]

    class Config(BaseConfig):
        pass


class Signup(BaseModel):
    full_name: str
    username: str
    email: str
    password: str

    class Config(BaseConfig):
        pass


class UserOut(BaseModel):
    message: str
    data: UserBase

    class Config(BaseConfig):
        pass


# Token
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int


class SessionOut(BaseModel):
    id: int
    user_id: int
    user_agent: Optional[str]
    ip_address: Optional[str]
    created_at: datetime
    expires_at: datetime
    is_active: bool

    class Config(BaseConfig):
        pass
