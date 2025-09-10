from functools import lru_cache
from redis.asyncio import ConnectionPool
from redis.asyncio.client import Redis
from redis.exceptions import RedisError
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema
from fastapi.templating import Jinja2Templates

from settings import get_settings


# MongoDB
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


# Redis
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


async def SendOTPCode(to_email: str, otp: str):
    """
    send otp code to user by email.
    """

    settings = get_settings()

    template_path = Jinja2Templates(directory="templates_email")
    configs = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=int(settings.MAIL_PORT),
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )

    mail = FastMail(configs)
    template = template_path.get_template("otp.html")
    html_content = template.render({"otp": otp})

    message = MessageSchema(
        subject="Your OTP Code from Hotel Luxora",
        recipients=[to_email],
        body=html_content,
        subtype="html"
    )

    try:
        await mail.send_message(message)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
