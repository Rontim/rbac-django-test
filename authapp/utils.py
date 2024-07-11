import jwt
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


User = get_user_model()


def generate_access_token(user: AbstractUser):
    payload = {
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
        'iat': datetime.datetime.now(datetime.UTC),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def generate_refresh_token(user: AbstractUser):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7),
        'iat': datetime.datetime.now(datetime.UTC),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
