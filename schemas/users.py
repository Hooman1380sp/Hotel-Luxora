from typing import Optional, Annotated
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from pydantic.functional_validators import AfterValidator

from utils.validators import PasswordType, IranianPhoneNumberType


class UserRegister(BaseModel):
    email: EmailStr
    password: PasswordType


class UserVerify(BaseModel):
    code: str
    email: EmailStr

# class UserCreate(UserBase):
#     password: str
#
# class UserInDB(UserBase):
#     id: str
#     hashed_password: str
#     disabled: bool = False
#
#     class Config:
#         json_encoders = {ObjectId: str}
