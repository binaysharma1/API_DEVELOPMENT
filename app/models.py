from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
import sqlalchemy.sql.expression
from sqlalchemy.orm import relationship

#model for alchemy database 
class Post(Base):
    __tablename__ = "posts"
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    published = Column(Boolean, nullable=False, default=True, server_default=sqlalchemy.sql.expression.true())
    created_at=Column(DateTime(timezone=True),nullable=False, server_default=sqlalchemy.sql.expression.text('now()')) 
    owner_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) 
    owner = relationship("User", back_populates="posts")  # Establishes a relationship with the User model


#model that hold user information
class User(Base):
    __tablename__ = "users"
    id=Column(Integer, primary_key=True, index=True)
    email=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)
    created_at=Column(DateTime(timezone=True),nullable=False, server_default=sqlalchemy.sql.expression.text('now()'))
    posts = relationship("Post", back_populates="owner")