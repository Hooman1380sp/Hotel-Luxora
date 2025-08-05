from random import randint

from settings import get_settings


# def connection_db(collection_name):
#     settings = get_settings()
#     db = settings.mongo_db
#     collection = db[str(collection_name)]
#     return collection
    
connection_db = lambda collection_name: get_settings().mongo_db[str(collection_name)]

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