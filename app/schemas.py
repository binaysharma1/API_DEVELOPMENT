from pydantic import BaseModel, ConfigDict
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
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: str
    password: str
    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)

class UserAuth(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    message: str

class SignupResponse(BaseModel):
    message: str



class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None