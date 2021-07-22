import pytz
from django.utils import timezone
from rest_framework import serializers

from .models import Answer, Prediction, Question, Reply, Vote


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
        if simple:
            return {
                "id": reply.id,
                "question": {"id": reply.question.id},
                "vote": {"id": reply.vote.id, "answer": reply.vote.answer.id},
                "prediction": {
                    "id": reply.prediction.id,
                    "answer": reply.prediction.answer.id,
                },
            }
        return {
            "id": reply.id,
            "question": {
                "id": reply.question.id,
                "content": reply.question.content,
                "answers": [
                    {"id": answer.id, "content": answer.content}
                    for answer in reply.question.answers.all()
                ],
            },
            "vote": {"id": reply.vote.id, "answer": reply.vote.answer.id},
            "prediction": {
                "id": reply.prediction.id,
                "answer": reply.prediction.answer.id,
            },
        }

    @staticmethod
    def invalid_answer(question, valid_answers):
        raise serializers.ValidationError(
            f"Answers must be one of the following for question {question.id}: "
            f"{[answer.id for answer in valid_answers]}"
        )

    def get(self, request):
        replies = Reply.objects.filter(user_id=request.user.id)
        simple = "full" not in request.query_params
        return [self.format_reply(reply, simple=simple) for reply in replies]

    def create(self, validated_data):
        existing_reply = Reply.objects.filter(
            user_id=validated_data["user_id"],
            question_id=validated_data["question_id"],
        ).first()
        try:
            question = Question.objects.filter(
                start_date__lte=timezone.datetime.now(pytz.utc),
                end_date__gte=timezone.datetime.now(pytz.utc),
            ).get(id=validated_data["question_id"])
        except Question.DoesNotExist:
            raise serializers.ValidationError(
                f"Question {validated_data['question_id']} is not active or does not exist"
            )
        valid_answers = question.answers.all()
        try:
            voted_answer = Answer.objects.get(id=validated_data["vote_id"])
            predicted_answer = Answer.objects.get(id=validated_data["prediction_id"])
        except Answer.DoesNotExist:
            self.invalid_answer(question, valid_answers)
        for answer in [voted_answer, predicted_answer]:
            if answer not in valid_answers:
                self.invalid_answer(question, valid_answers)
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
