import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_data = request.headers.get('Authorization', None)

        if not auth_data:
            return None

        auth_data = auth_data.split()

        if len(auth_data) != 2:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid, login')

        if auth_data[0].lower() != 'bearer':
            raise exceptions.AuthenticationFailed(
                'Your token is invalid, login')

        token = auth_data[1]

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if payload['role'] != user.role:
                raise exceptions.AuthenticationFailed(
                    'Your token is invalid, login')

            request.role = payload['role']

            return (user, token)
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid, login')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is expired, login')
        except jwt.InvalidTokenError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid, login')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        raise exceptions.AuthenticationFailed('Your token is invalid, login')
