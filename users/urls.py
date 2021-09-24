from django.urls import path

from . import views

urlpatterns = [
    path("create-user/", views.CreateUserView.as_view()),
    path("get-user/", views.UserDetailView.as_view()),
]
