"""
Vote Predict project - URL Configuration

Configured for Django 3
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("votepredictapp.urls")),
    path("", include("users.urls")),
    path("api-token-auth/", views.obtain_auth_token),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
