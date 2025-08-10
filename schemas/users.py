from pydantic import BaseModel, EmailStr
from typing import Optional, Annotated
from bson import ObjectId
from pydantic import BaseModel, EmailStr
from pydantic.functional_validators import AfterValidator

from utils.utils import validate_password_complexity, validate_iranian_mobile

PasswordType = Annotated[str, AfterValidator(validate_password_complexity)]
IranianPhoneNumberType = Annotated[str, AfterValidator(validate_iranian_mobile)]


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
