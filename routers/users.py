from typing import Annotated
import json
from fastapi import APIRouter, Body, Depends, status, HTTPException, BackgroundTasks, Response
from random import randint
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.utils import collection_db, get_db, get_redis, SendOTPCode
from schemas.users import UserRegister

router = APIRouter()


@router.post('/api/user-register/', response_model=UserRegister, status_code=status.HTTP_201_CREATED)
async def UserRegister(background_task: BackgroundTasks,
                       user: UserRegister = Body(),
                       db: AsyncIOMotorCollection = Depends(get_db)):
    user_collection = collection_db("User", db=db)
    email = str(user.email)
    if await user_collection.find_one({"email": email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist")

    otp = str(randint(1000, 9999))
    redis = get_redis()
    await redis.setex(name=otp, time=60 * 2, value={"email": email, "otp_code": otp})
    background_task.add_task(SendOTPCode, email, otp)
    # return Response(
    #     status_code=status.HTTP_201_CREATED,
    #     content=json.dumps({
    #         "message": "OTP sent successfully",
    #         "email": email
    #     }),
    #     media_type="application/json"
    # )
    return email
