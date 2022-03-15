from pydantic import BaseModel, EmailStr
from typing import Optional


class UserItems(BaseModel):
    email: EmailStr
    username: str
    password: str


class GetUser(BaseModel):
    email: EmailStr


class ServerItems(BaseModel):
    # email: EmailStr
    # username: str
    server_group: str


class GroupItems(BaseModel):
    email: EmailStr
    username: str
    server_group: str
    admin: bool


class InviteItems(BaseModel):
    invited_to: str
    user: EmailStr


class ServerDetailsItems(BaseModel):
    ip_address: str
    server_group: str
    # created_by: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserList(BaseModel):
    email: str
