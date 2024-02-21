from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint
class Userout(BaseModel):
    id:int
    email:EmailStr
    class Config:
        orm_mode=True
class Post(BaseModel):#schema for Post method
    title:str
    content:str
    published:bool=True
    rating:Optional[int]=None
class Createpost(Post):
    pass
class PostResponse(Post):
    created_at:datetime
    owner_id:int
    owner:Userout
    class Config:
        orm_mode=True
class PostVote(BaseModel):
    Posts:PostResponse
    likes:int
    class Config:
        orm_mode=True
class Createuser(BaseModel):
    email:EmailStr
    password:str        
# class Userout(BaseModel):
#     id:int
#     email:EmailStr
#     class Config:
#         orm_mode=True
class Userlogin(BaseModel):
    email:EmailStr
    password:str
class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    id:Optional[str]=None
class Vote(BaseModel):
    posts_id:int
    dir: conint(ge=0,le=1)