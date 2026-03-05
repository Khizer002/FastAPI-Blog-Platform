from pydantic import BaseModel,EmailStr
from pydantic.types import conint
from typing import Optional
from datetime import datetime

class Blog(BaseModel):
    title:str
    content:str
    published:bool=True
    # rating:Optional[int]=None

class insert_blog(Blog):
    pass

class updateBlog(BaseModel):
    title:Optional[str]=None
    content:Optional[str]=None
    published:Optional[str]=None

class User_Response(BaseModel):
    id:int
    email:EmailStr
    fullName:str
    created_At:datetime

    class Config:
        from_attributes=True
        
class Response_blogs(Blog):
    id: int
    created_At:datetime
    owner_id: int
    owner:User_Response

    class Config:
        from_attributes = True


class BlogOut(BaseModel):
    Blog: Response_blogs
    likes: int

    class Config:
        from_attributes = True

class Create_User(BaseModel):
    fullName:str
    email:EmailStr
    password:str

class Login_User(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class Vote(BaseModel):
    post_id:int
    dir:int