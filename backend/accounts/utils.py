import random
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed

OTP_TTL_SECONDS = 300  # 5 minutes


def generate_otp() -> str:
    """
    Generate a random 6-digit one-time password (OTP).

    Returns:
        str: A 6-digit OTP code as a string.
    """
    return f"{random.randint(100000, 999999)}"


def otp_cache_key(email: str) -> str:
    """
    Generate a cache key for storing OTPs based on the user's email.

    Args:
        email (str): The user's email address.

    Returns:
        str: A string cache key in the format "otp:<email>".
    """
    return f"otp:{email}"


def store_otp(email: str, code: str) -> None:
    """
    Store an OTP in the cache with a defined TTL (time-to-live).

    Args:
        email (str): The user's email address.
        code (str): The OTP code to store.

    Returns:
        None
    """
    cache.set(otp_cache_key(email), code, timeout=OTP_TTL_SECONDS)


def verify_otp(email: str, code: str) -> bool:
    """
    Verify if the provided OTP matches the one stored in cache.

    Args:
        email (str): The user's email address.
        code (str): The OTP code provided by the user.

    Returns:
        bool: True if OTP matches, False otherwise.
    """
    stored = cache.get(otp_cache_key(email))
    return stored == code


def clear_otp(email: str) -> None:
    """
    Remove an OTP from the cache after successful verification or expiration.

    Args:
        email (str): The user's email address.

    Returns:
        None
    """
    cache.delete(otp_cache_key(email))


def name_from_email(email: str) -> str:
    """
    Generate a human-readable name from an email address.

    This function takes the local part of the email (before '@'), replaces
    dots and underscores with spaces, and capitalizes each word.

    Args:
        email (str): The user's email address.

    Returns:
        str: A formatted name derived from the email.
    
    Example:
        >>> name_from_email("john.doe_example@gmail.com")
        'John Doe Example'
    """
    local = email.split("@")[0]
    cleaned = local.replace(".", " ").replace("_", " ")
    return " ".join(word.capitalize() for word in cleaned.split())


def get_tokens_for_user(user):
    """
    Generate JWT access and refresh tokens for a given user.

    Args:
        user (User): A Django User model instance.

    Returns:
        dict: A dictionary containing:
            - 'refresh' (str): The JWT refresh token.
            - 'access' (str): The JWT access token.

    Raises:
        AuthenticationFailed: If the user is inactive and cannot authenticate.
    """
    if not user.is_active:
        raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

