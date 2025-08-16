from functools import lru_cache
from random import randint
from redis.asyncio import ConnectionPool
from redis.asyncio.client import Redis
from redis.exceptions import RedisError
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from settings import get_settings


@lru_cache(maxsize=None)
def get_db() -> AsyncIOMotorDatabase:
    settings = get_settings()
    return settings.mongo_db


@lru_cache(maxsize=10)
def collection_db(collection_name: str, db) -> AsyncIOMotorCollection:
    """connection to mongodb. cached by @alru_cache library with maximum ten(10) size place in memory"""
    try:
        collection = db[str(collection_name)]
        return collection
    except Exception as e:
        # logging.error(
        #     f"Failed to get collection '{collection_name}': {str(e)}",
        #     exc_info=True  # جزئیات کامل خطا (شامل traceback)
        # )
        raise e


@lru_cache(maxsize=None)
def get_redis():
    """
    get (return) instance of Redis.
   (we save it ar memory cache because we`re going to use it a lot)
    """
    try:
        settings = get_settings()
        # Redis connection pool
        redis_pool = ConnectionPool.from_url(
            settings.REDIS_URL,
            max_connections=120,
            decode_responses=True
        )
        redis = Redis(connection_pool=redis_pool)
        return redis
    except RedisError as e:
        # logger.error(f"Redis connection failed: {e}")
        raise e


class OtpHandler:
    """
    This handler is responsible for creating and verifying otp codes.
    """

    @staticmethod
    async def create() -> int:
        """Hash password using bcrypt"""
        return randint(11111, 99999)

    @staticmethod
    async def validate(otp: int, user: dict) -> bool:
        """Validate otp code"""
        user_otp = user.get('otp')
        return int(otp) == int(user_otp)
