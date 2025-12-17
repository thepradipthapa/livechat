from django.core.cache import cache

# Limits
OTP_PER_MINUTE = 1       # Max OTP requests per minute per email
VERIFY_PER_CODE = 3      # Max verification attempts per OTP code

# Time windows
ONE_MINUTE = 60          # seconds
OTP_TTL = 300            # seconds (5 minutes)

def can_send_otp(email: str) -> bool:
    """
    Check if the user can request a new OTP based on rate limits.

    Args:
        email (str): The user's email address.

    Returns:
        bool: True if the OTP request is allowed, False if rate limits are exceeded.
    """
    ratelimit_key = f"ratelimit:send:otp:{email}"

    # Per-minute limit
    if cache.get(ratelimit_key):
        return False

    # Update counters
    cache.set(ratelimit_key, 1, timeout=ONE_MINUTE)

        
    return True


def can_verify_otp(email: str, otp: str) -> bool:
    """
    Check if the user can verify an OTP based on rate limits.

    Args:
        email (str): The user's email address.
        otp (str): The OTP code being verified.
        
    Returns:
        bool: True if the OTP verification is allowed, False if rate limits are exceeded.
    """
    ratelimit_key = f"ratelimit:verify:otp:{email}:{otp}"

    code_attempts = cache.get(ratelimit_key)
    if code_attempts is None:
        
        cache.set(ratelimit_key, 1, timeout=OTP_TTL)
        return True

    if code_attempts >= VERIFY_PER_CODE:
        return False
    
    cache.incr(ratelimit_key)
    return True
