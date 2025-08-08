from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str  # admin, reception, user

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str
    hashed_password: str
    disabled: bool = False

    class Config:
        json_encoders = {ObjectId: str}