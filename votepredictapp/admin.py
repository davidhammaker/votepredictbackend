from django.contrib import admin

from .models import Answer, Prediction, Question, Reply, Vote


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["content", "start_date", "end_date"]
    fields = ["content", "start_date", "end_date"]
    inlines = [AnswerInline]


class VoteInline(admin.StackedInline):
    model = Vote


class PredictionInline(admin.StackedInline):
    model = Prediction


class ReplyAdmin(admin.ModelAdmin):
    list_display = ["question", "vote", "prediction", "user"]
    model = Reply
    inlines = [VoteInline, PredictionInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Reply, ReplyAdmin)
