from typing import Annotated

from fastapi import APIRouter, Body, Depends, status, HTTPException
from utils.utils import connection_db, get_db
from motor.motor_asyncio import AsyncIOMotorCollection
from schemas.users import UserRegister

router = APIRouter()


@router.post('/api/user-register/', response_model=UserRegister, status_code=status.HTTP_201_CREATED)
async def UserRegister(user: UserRegister = Body(),
                       db: AsyncIOMotorCollection = Depends(get_db)):
    # if await collection.find_one({"email": user.email}):
    #     raise HTTPException(400, "Email exists")
