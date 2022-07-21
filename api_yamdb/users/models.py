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
        validators=[username_validator, ], blank=False
    )
    email = models.EmailField(max_length=254, unique=True, blank=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(("role"), choices=Roles.choices(), default="user",
                            max_length=50)
    confirmation_code = models.CharField(max_length=36, blank=True)
    is_active = models.BooleanField(default=False)

    confirmation_code = models.CharField(max_length=36, blank=True)
    USERNAME_FIELD = 'username'

    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'access': str(refresh.access_token)}
    
    def is_admin(self):
        return self.role == admin
    
    def is_moderator(self):
        return self.role == moderator
        

    def __str__(self):
        return self.email
