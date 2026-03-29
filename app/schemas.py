from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Annotated
from datetime import datetime
from fastapi import Body
from . import dependencies as deps

class Blog(BaseModel):
    title: deps.Title
    content: deps.Content
    published: deps.Published = True
    # rating:Optional[int]=None

class insert_blog(Blog):
    pass

class updateBlog(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class User_Response(BaseModel):
    id: int
    email: EmailStr
    fullName: str
    created_At: datetime

    class Config:
        from_attributes = True
        
class Response_blogs(Blog):
    id: int
    created_At: datetime
    owner_id: int
    owner: User_Response

    class Config:
        from_attributes = True

class BlogOut(BaseModel):
    Blog: Response_blogs
    likes: int

    class Config:
        from_attributes = True

class Create_User(BaseModel):
    fullName: deps.FullName
    email: EmailStr
    password: deps.PASSWORD

    @field_validator('password')
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class Login_User(BaseModel):
    email: EmailStr
    password: deps.PASSWORD

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

class Vote(BaseModel):
    post_id: deps.BlogID
    dir: deps.DirID

Payload = Annotated[insert_blog, Body(description="The Blog data")]
update_blog_data = Annotated[Blog, Body(description="Data to be updated")]
AddUser = Annotated[Create_User, Body(description="Data to create a user")]
AddVote = Annotated[Vote, Body(description="Data required to like a post")]