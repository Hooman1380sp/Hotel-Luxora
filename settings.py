from pydantic_settings import BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient
from functools import lru_cache, cached_property


class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DB_NAME: str

    class Config:
        env_file = ".env"

    @cached_property
    def mongo_client(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(self.MONGO_URI)

    @cached_property
    def mongo_db(self):
        return self.mongo_client.get_database(self.MONGO_DB_NAME)


@lru_cache()
def get_settings() -> Settings:
    return Settings()