from pydantic import BaseModel
import datetime as _dt

class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True

class LoginUser(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    date_created: _dt.datetime
    class Config:
        orm_mode = True
