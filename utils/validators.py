import re
from pydantic import ValidationError
from pydantic.functional_validators import AfterValidator
from typing import Annotated


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


PasswordType = Annotated[str, AfterValidator(validate_password_complexity)]
IranianPhoneNumberType = Annotated[str, AfterValidator(validate_iranian_mobile)]
