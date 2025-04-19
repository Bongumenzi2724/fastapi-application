from pydantic import BaseModel,EmailStr
from sqlalchemy.sql.functions import mode
from typing import Optional
from pydantic.types import conint

#Pydantic model for request data validation
class PostSchema(BaseModel):
    title:str
    content:str
    #optional field the user can provide a published if not it will default to True
    published:bool=True

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True
    
class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class UserResponse(BaseModel):
    email:str
    id:int
    class config:
        orm_mode=mode


class PostResponse(PostBase):
    owner_id:int
    owner:UserResponse


class PostOut(PostBase):
    post:PostResponse
    votes:int
 

class UserSchema(BaseModel):
    email:EmailStr
    password:str  
    


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None
    


class VoteSchema(BaseModel):
    post_id:int
    dir:int

