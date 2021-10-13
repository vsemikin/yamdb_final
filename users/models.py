from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"


ROLES = ((USER, "user"), (MODERATOR, "moderator"), (ADMIN, "admin"))


class User(AbstractUser):
    email = models.EmailField("email address", unique=True)
    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer."
            "Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "A user with that username already exists.",
        },
        blank=True,
        null=True,
    )
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField("name", max_length=30, blank=True, null=True)
    last_name = models.CharField(
        "surname", max_length=30, blank=True, null=True
    )
    bio = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(choices=ROLES, default=USER, max_length=30)
    password = models.TextField("password")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", ]

    class Meta:
        ordering = ["-id"]

    @property
    def check_role(self):
        return self.role in (MODERATOR, ADMIN)

    def __str__(self):
        return self.email


class ConfirmationCode(models.Model):
    email = models.EmailField("email address", unique=True)
    confirmation_code = models.CharField(max_length=20)
