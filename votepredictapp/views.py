from django.utils import timezone
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


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.filter(
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now(),
    )

    @action(detail=False)
    def closed(self, _request):
        closed_questions = Question.objects.all().filter(
            end_date__lte=timezone.now()
        )
        serializer = self.get_serializer(closed_questions, many=True)
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
