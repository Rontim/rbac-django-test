from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls')),
    path('google-auth/', include('rest_auth.urls')),
    path('google-auth/registration/', include('rest_auth.registration.urls')),
    path('google-auth/social/', include('allauth.urls')),
]
