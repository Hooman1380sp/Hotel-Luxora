import re
from functools import lru_cache
from random import randint
from pydantic import ValidationError
from redis.asyncio import ConnectionPool
from redis.asyncio.client import Redis
from redis.exceptions import RedisError

from settings import get_settings


@lru_cache(maxsize=10)
def connection_db(collection_name: str):
    """connection to mongodb"""
    settings = get_settings()
    db = settings.mongo_db
    collection = db[str(collection_name)]
    return collection


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


def validate_password_complexity(password: str) -> str:
    """Validate Password"""
    if len(password) < 8 or len(password) > 22:
        raise ValidationError("Password must be between 8 and 22 characters")

    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter")

    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter")

    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one digit")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must contain at least one special character")
    return password


def validate_iranian_mobile(mobile: str) -> str:
    """Validate Iranian mobile number format"""

    cleaned = re.sub(r'[^\d]', '', mobile)
    if len(cleaned) != 11:
        raise ValidationError("Mobile number must be 11 digits")

    if not cleaned.startswith('09'):
        raise ValidationError("Mobile number must start with 09")

    if not cleaned.isdigit():
        raise ValidationError("Mobile number must contain only digits")

    valid_prefixes = ['090', '091', '092', '093', '099']
    if cleaned[:3] not in valid_prefixes:
        raise ValidationError("Invalid mobile prefix")
    return cleaned
