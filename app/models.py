from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,VARCHAR,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func

class Blog(Base):
    __tablename__="blogs"
    id=Column(Integer,primary_key=True)
    title=Column(VARCHAR(100),nullable=False)
    content=Column(VARCHAR(100),nullable=False)
    published=Column(Boolean,nullable=False,server_default='1')
    created_At=Column(TIMESTAMP, nullable=False, server_default=func.now())
    owner_id=Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner=relationship("User")

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    fullName=Column(VARCHAR(100), nullable=False)
    email=Column(VARCHAR(100), nullable=False, unique=True)
    password=Column(VARCHAR(200), nullable=False)
    created_At=Column(TIMESTAMP, nullable=False, server_default=func.now())

class Vote(Base):
    __tablename__="votes"
    post_id=Column(Integer,ForeignKey("blogs.id",ondelete="CASCADE"),primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)

class RefreshToken(Base):
    __tablename__="refresh_tokens"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    token=Column(VARCHAR(255),unique=True,nullable=False)
    is_used=Column(Boolean,nullable=False,server_default="0")
    created_At=Column(TIMESTAMP,nullable=False,server_default=func.now())
