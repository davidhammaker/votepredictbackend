from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"questions", views.QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("reply/", views.ReplyView.as_view()),
]
