from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken
from users.enums import Roles


class CustomUser(AbstractUser):

    username_validator = RegexValidator(
        regex=r'^(?!me$)^[\w.@+-]+$',
        message=(
            "Username должен содержать только буквы, "
            "цифры и символы: '@', '.', '+', '-', '_'"
            "и не me"
        )
    )

    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[username_validator, ], required=False
    )
    email = models.EmailField(max_length=254, unique=True, required=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(("role"), choice=Roles.choices(), default="user")
    confirmation_code = models.CharField(max_length=36, blank=True)
    is_active = models.BooleanField(default=False)
    is_moderator = models.BooleanField(('moderator'), default=False,)
    is_admin = models.BooleanField(('admin'), default=False,)
    confirmation_code = models.CharField(max_length=36, blank=True)
    USERNAME_FIELD = 'username'

    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'access': str(refresh.access_token)}

    def __str__(self):
        return self.email
