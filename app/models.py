from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
import sqlalchemy.sql.expression

#model for alchemy database 
class Post(Base):
    __tablename__ = "posts"
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean, default=True)
    created_at=Column(DateTime(timezone=True),nullable=False, server_default=sqlalchemy.sql.expression.text('now()')) 



#model that hold user information
class User(Base):
    __tablename__ = "users"
    id=Column(Integer, primary_key=True, index=True)
    email=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)
    created_at=Column(DateTime(timezone=True),nullable=False, server_default=sqlalchemy.sql.expression.text('now()'))