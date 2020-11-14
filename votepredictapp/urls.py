from django.urls import path

from . import views as votepredictapp_views

urlpatterns = [
    path(
        "questions/", votepredictapp_views.QuestionList.as_view(), name="question-list"
    ),
    path("answers/", votepredictapp_views.AnswerList.as_view(), name="answer-list"),
    path("replies/", votepredictapp_views.ReplyList.as_view(), name="reply-list"),
    path("votes/", votepredictapp_views.VoteList.as_view(), name="vote-list"),
    path(
        "predictions/",
        votepredictapp_views.PredictionList.as_view(),
        name="prediction-list",
    ),
]
