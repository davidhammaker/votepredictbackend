from datetime import datetime  # TODO: Make sure utcnow works well

from django.utils import timezone
from rest_framework import views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Answer, Prediction, Question, Reply, Vote
from .serializers import QuestionSerializer, ReplySerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.filter(
        start_date__lte=datetime.utcnow(),
        end_date__gte=datetime.utcnow(),
    )

    @action(detail=False)
    def closed(self, _request):
        closed_questions = Question.objects.all().filter(
            end_date__lte=datetime.utcnow()
        )
        serializer = self.get_serializer(closed_questions, many=True)
        return Response(serializer.data)


class ReplyView(views.APIView):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        return Response(serializer.get(request))

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # The following method saves request.data automatically. I
            # am manually adding user_id to be included in
            # validated_data in the create() method of the serializer.
            serializer.save(user_id=request.user.id)
            return Response(serializer.instance)
        return Response(serializer.errors, 400)
