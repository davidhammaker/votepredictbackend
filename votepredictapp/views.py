from datetime import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Answer, Prediction, Question, Reply, Vote
from .serializers import (
    AnswerSerializer,
    PredictionSerializer,
    QuestionSerializer,
    ReplySerializer,
    VoteSerializer,
)


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    @action(detail=False)
    def active(self, _request):
        active_questions = Question.objects.all().filter(
            start_date__lte=datetime.today(),
            end_date__gte=datetime.today()
        )
        serializer = self.get_serializer(active_questions, many=True)
        return Response(serializer.data)


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class ReplyViewSet(viewsets.ModelViewSet):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()


class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()


class PredictionViewSet(viewsets.ModelViewSet):
    serializer_class = PredictionSerializer
    queryset = Prediction.objects.all()
