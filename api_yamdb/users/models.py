from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .utils import set_confirmation_code
from .validators import me_username_validator


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPERUSER = "superuser"

    ROLES = [
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
        (SUPERUSER, "superuser"),
    ]

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="username",
        help_text=(
            "Required. 150 characters or fewer."
            "Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator, me_username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    email = models.EmailField(
        unique=True,
        verbose_name="email",
        help_text="User's email",
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    bio = models.TextField(
        max_length=2048,
        blank=True,
        verbose_name="Bio",
        help_text="User's bio",
    )
    role = models.CharField(
        max_length=16,
        verbose_name="Role",
        help_text="User's role",
        choices=ROLES,
        default=USER
    )
    confirmation_code = models.CharField(
        max_length=16,
        unique=True,
        default=set_confirmation_code,
        verbose_name="confirmation_code",
        help_text="Confirmation code"
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_super(self):
        return self.role == self.SUPERUSER or self.is_superuser

    class Meta(AbstractUser.Meta):
        ordering = ("-id",)
        constraints = (
            models.UniqueConstraint(
                fields=("email", "username"),
                name="email_username_uniqueness_constraint"
            ),
            models.CheckConstraint(
                check=~models.Q(username="me"),
                name="username_<me>_is_prohibited"
            ),
        )
