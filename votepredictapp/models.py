from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    content = models.CharField(max_length=128)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)


class Answer(models.Model):
    content = models.CharField(max_length=128)
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )


class Reply(models.Model):
    question = models.ForeignKey(
        Question, related_name="replies", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, related_name="replies", on_delete=models.CASCADE)


class Vote(models.Model):
    reply = models.OneToOneField(Reply, related_name="vote", on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name="votes", on_delete=models.CASCADE)


class Prediction(models.Model):
    reply = models.OneToOneField(
        Reply, related_name="prediction", on_delete=models.CASCADE
    )
    answer = models.ForeignKey(
        Answer, related_name="predictions", on_delete=models.CASCADE
    )
