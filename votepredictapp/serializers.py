from rest_framework import serializers

from .models import Answer, Prediction, Question, Reply, Vote


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        fields = ["id", "start_date", "end_date", "content", "answers"]
        model = Question

    def get_answers(self, obj):
        return [
            {"id": answer.id, "content": answer.content} for answer in obj.answers.all()
        ]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "question", "content"]
        model = Answer


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "question", "vote", "prediction", "user"]
        model = Reply


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "reply", "answer"]
        model = Vote


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "reply", "answer"]
        model = Prediction
