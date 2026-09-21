from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
   
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostDelete(BaseModel):
    id: int
    title: str



class Post(PostBase):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: str
    password: str
    class Config:
        orm_mode = True

class User(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class UserAuth(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    message: str



class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None