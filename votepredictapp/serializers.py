import pytz
from django.utils import timezone
from rest_framework import serializers

from .models import Prediction, Question, Reply, Vote


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        fields = ["id", "start_date", "end_date", "content", "answers"]
        model = Question

    @staticmethod
    def get_answers(obj):
        return [
            {"id": answer.id, "content": answer.content} for answer in obj.answers.all()
        ]


class ReplySerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=True)
    vote_id = serializers.IntegerField(required=True)
    prediction_id = serializers.IntegerField(required=True)
    user = serializers.ReadOnlyField()

    @staticmethod
    def format_reply(reply, simple=False):
        response = {
            "id": reply.id,
            "question": {"id": reply.question.id},
            "vote": {"id": reply.vote.id, "answer": reply.vote.answer.id},
            "prediction": {
                "id": reply.prediction.id,
                "answer": reply.prediction.answer.id,
            },
        }
        if simple:
            return response
        response["question"]["content"] = reply.question.content
        response["question"]["answers"] = [
            {"id": answer.id, "content": answer.content}
            for answer in reply.question.answers.all()
        ]
        return response

    def get(self, request):
        replies = Reply.objects.filter(user_id=request.user.id)
        simple = "full" not in request.query_params
        return [self.format_reply(reply, simple=simple) for reply in replies]

    def create(self, validated_data):
        existing_reply = Reply.objects.filter(
            user_id=validated_data["user_id"],
            question_id=validated_data["question_id"],
        ).first()
        question = Question.objects.filter(
            start_date__lte=timezone.datetime.now(pytz.utc),
            end_date__gte=timezone.datetime.now(pytz.utc),
            id=validated_data["question_id"],
        ).first()
        if not question:
            raise serializers.ValidationError(
                {
                    "detail": f"Question {validated_data['question_id']} is not active "
                    f"or does not exist"
                }
            )
        voted_answer = question.answers.filter(id=validated_data["vote_id"]).first()
        predicted_answer = question.answers.filter(
            id=validated_data["prediction_id"]
        ).first()
        for answer in [voted_answer, predicted_answer]:
            if not answer:
                raise serializers.ValidationError(
                    {
                        "detail": f"Answers must be one of the following for question "
                        f"{question.id}: "
                        f"{[answer.id for answer in question.answers.all()]}"
                    }
                )
        if existing_reply:
            vote = Vote.objects.get(reply=existing_reply)
            vote.answer = voted_answer
            vote.save()
            prediction = Prediction.objects.get(reply=existing_reply)
            prediction.answer = predicted_answer
            prediction.save()
            reply = existing_reply
        else:
            reply = Reply(
                user_id=validated_data["user_id"],
                question_id=validated_data["question_id"],
            )
            reply.save()
            vote = Vote(answer=voted_answer, reply=reply)
            prediction = Prediction(answer=predicted_answer, reply=reply)
            vote.save()
            prediction.save()
        return self.format_reply(reply)

    def update(self, instance, validated_data):
        pass
