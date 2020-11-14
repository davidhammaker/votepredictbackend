from rest_framework import generics

from .models import Answer, Prediction, Question, Reply, Vote
from .serializers import (
    AnswerSerializer,
    PredictionSerializer,
    QuestionSerializer,
    ReplySerializer,
    VoteSerializer,
)


class QuestionList(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class AnswerList(generics.ListCreateAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class ReplyList(generics.ListCreateAPIView):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()


class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()


class PredictionList(generics.ListCreateAPIView):
    serializer_class = PredictionSerializer
    queryset = Prediction.objects.all()
