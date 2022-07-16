import email
from pydantic import BaseModel
from typing import Optional, List, Union


class BlogSchema(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True


class UserSchema(BaseModel):
    name: str
    email: str
    password: str

class ShowUserSchema(BaseModel):
    name: str
    email: str


    class Config():
        orm_mode = True

class BaseUserSchema(BaseModel):
    name: str
    email: str
    blog: List[BlogSchema]
    class Config():
        orm_mode = True


class ShowBlogSchema(BaseModel):
    title: str
    body: str
    created_by: ShowUserSchema

    class Config():
        orm_mode = True

class LoginSchema(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None