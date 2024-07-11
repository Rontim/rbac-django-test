from django.contrib.auth import get_user_model
from .serielizers import UserCreateSerializer, UserListSerializer, UserLoginSerializer
from .utils import generate_access_token, generate_refresh_token
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions, exceptions
from django.contrib.auth import authenticate


User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if email is None:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        if password is None:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        authenticatation_kwargs = {
            "email": email,
            "password": password,
            "request": request
        }

        user = authenticate(**authenticatation_kwargs)

        access = generate_access_token(user)
        refresh = generate_refresh_token(user)

        return Response({'access': access, 'refresh': refresh}, status=status.HTTP_200_OK)
