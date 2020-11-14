from rest_framework import serializers

from .models import Answer, Prediction, Question, Reply, Vote


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "start_date", "end_date", "content", "answers"]
        model = Question


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
