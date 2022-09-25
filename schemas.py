import pydantic
import datetime

class UserBase(pydantic.BaseModel):
    email: str
    name: str
    phone: str

class UserRequset(UserBase):
    password: str
    class Config:
        orm_mode = True

class UserResponse(UserBase):
    id: int
    created_At: datetime.datetime
    class Config:
        orm_mode = True

class PostsBase(pydantic.BaseModel):
    title: str
    content: str   
    image : str

class PostsRequest(PostsBase):
    pass

class PostsResponse(PostsBase):
    id: int
    created_At: datetime.datetime
    class Config:
        orm_mode = True