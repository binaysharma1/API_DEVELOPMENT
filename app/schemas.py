from pydantic import BaseModel


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
    title: str
    content: str
    published: bool
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
    message: str