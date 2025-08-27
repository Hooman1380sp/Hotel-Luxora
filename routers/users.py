from typing import Annotated
from fastapi import APIRouter, Body, Depends, status, HTTPException
from utils.utils import collection_db, get_db, get_redis
from motor.motor_asyncio import AsyncIOMotorCollection
from schemas.users import UserRegister

router = APIRouter()


@router.post('/api/user-register/', response_model=UserRegister, status_code=status.HTTP_201_CREATED)
async def UserRegister(user: UserRegister = Body(),
                       db: AsyncIOMotorCollection = Depends(get_db)):
    user_collection = collection_db("User", db=db)

    if await user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist")
