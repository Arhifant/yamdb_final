import os

from django.conf import settings
from django.core.mail import send_mail


def set_confirmation_code(size=settings.CONFIRMATION_CODE_BYTE_SIZE):
    """
    With UUID can not pass Yandex tests.
    """
    return os.urandom(size).hex()


def send_confirmation_code(user_obj):
    send_mail(
        "Confirmation code",
        f"Your confirmation code is {user_obj.confirmation_code}.",
        settings.ADMIN_EMAIL,
        [user_obj.email],
    )
