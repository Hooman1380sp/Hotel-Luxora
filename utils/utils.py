from random import randint
from functools import lru_cache
from redis.asyncio import ConnectionPool
from redis.asyncio.client import Redis
from redis.exceptions import RedisError

from settings import get_settings


def connection_db(collection_name):
    """connection to mongodb"""
    settings = get_settings()
    db = settings.mongo_db
    collection = db[str(collection_name)]
    return collection

# connection_db = lambda collection_name: get_settings().mongo_db[str(collection_name)]

@lru_cache()
def get_redis():
    """get (return) instance of Redis"""
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