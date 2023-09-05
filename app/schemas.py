from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    
    
    class Config:
        orm_mode = True
    


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None

#this code is working

# class Post(PostBase):
#     title: str
#     content: str
#     published: bool
    

#     class Config:
#         orm_mode = True

