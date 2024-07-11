from django.urls import path
from .views import UserCreateAPIView, UserLoginAPIView, UserListAPIView

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('users/', UserListAPIView.as_view(), name='users'),
]
