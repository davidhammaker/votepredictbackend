import pytz
from django.utils import timezone
from rest_framework import views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Question, Reply
from .serializers import QuestionSerializer, ReplySerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.filter(
        start_date__lte=timezone.datetime.now(pytz.utc),
        end_date__gte=timezone.datetime.now(pytz.utc),
    )

    @action(detail=False)
    def closed(self, _request):
        closed_questions = Question.objects.all().filter(
            end_date__lte=timezone.datetime.now(pytz.utc)
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
        return Response({"detail": serializer.errors[0]}, 400)


class TotalsView(views.APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def format_totals(question, request):
        # TODO: Consider creating a model for "totals"
        totals = {answer.id: answer.votes.count() for answer in question.answers.all()}
        question_final = {
            "id": question.id,
            "content": question.content,
            "answers": [
                {"id": answer.id, "content": answer.content}
                for answer in question.answers.all()
            ],
            "totals": totals,
        }
        reply = Reply.objects.filter(
            question_id=question.id, user_id=request.user.id
        ).first()
        if reply:
            question_update = {
                "vote": reply.vote.answer.id,
                "prediction": reply.prediction.answer.id,
                "correct_prediction": totals[reply.prediction.answer.id]
                == max(totals.values()),
            }
            question_final.update(question_update)
        return question_final

    def get(self, request):
        questions = Question.objects.filter(
            end_date__lte=timezone.datetime.now(pytz.utc)
        ).all()
        question_totals = list()
        correct_predictions = 0
        for question in questions:
            question_total = self.format_totals(question, request)
            question_totals.append(question_total)
            if question_total.get("correct_prediction"):
                correct_predictions += 1
        return Response(
            {"questions": question_totals, "correct_predictions": correct_predictions}
        )
