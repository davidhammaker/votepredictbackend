from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"questions", views.QuestionViewSet)
router.register(r"answers", views.AnswerViewSet)
router.register(r"replies", views.ReplyViewSet)
router.register(r"votes", views.VoteViewSet)
router.register(r"predictions", views.PredictionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
