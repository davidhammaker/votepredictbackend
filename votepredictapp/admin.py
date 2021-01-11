from django.contrib import admin

from .models import Answer, Question


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["content", "start_date", "end_date"]
    fields = ["content", "start_date", "end_date"]
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
