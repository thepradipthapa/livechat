# users/tasks.py
from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings

@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_otp_email_task(self, email: str, code: str):
    """
    Send a one-time password (OTP) to a user's email address.

    This Celery task sends an OTP email asynchronously to avoid blocking the main
    request/response cycle. It retries up to `max_retries` times with a delay of 
    `default_retry_delay` seconds in case of failures (e.g., SMTP errors).

    Args:
        email (str): The recipient's email address.
        code (str): The OTP code to send.

    Raises:
        self.retry: Retries the task if email sending fails.

    Returns:
        None
    """
    try:
        send_mail(
            subject="Your OTP code",
            message=f"Your OTP is {code}. It expires in 5 minutes.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as exc:
        raise self.retry(exc=exc)
