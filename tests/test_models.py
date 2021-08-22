from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from votepredictapp.models import Answer, Prediction, Question, Reply, Vote


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.start_date = timezone.now()
        self.sample_question = Question(
            content="sample content",
            start_date=self.start_date,
            end_date=self.start_date + timedelta(days=1),
        )
        self.sample_user = User(username="sample_user")
        self.sample_answer = Answer(content="sample answer content", question=self.sample_question)
        self.sample_reply = Reply()

    def test_new_question(self):
        start_date = self.start_date
        end_date = start_date + timedelta(days=7)
        question = Question(
            content="sample content",
            start_date=start_date,
            end_date=end_date,
        )
        assert str(question) == question.content
        assert question.content == "sample content"
        assert question.start_date == start_date
        assert question.end_date == end_date

    def test_new_answer(self):
        answer = Answer(content="sample content", question=self.sample_question)
        assert str(answer) == answer.question.content
        assert answer.content == "sample content"
        assert answer.question == self.sample_question

    def test_new_reply(self):
        reply = Reply(question=self.sample_question, user=self.sample_user)
        assert str(reply) == reply.question.content
        assert reply.question == self.sample_question
        assert reply.user == self.sample_user

    def test_new_vote(self):
        vote = Vote(reply=self.sample_reply, answer=self.sample_answer)
        assert str(vote) == vote.answer.content
        assert vote.reply == self.sample_reply
        assert vote.answer == self.sample_answer

    def test_new_prediction(self):
        prediction = Prediction(reply=self.sample_reply, answer=self.sample_answer)
        assert str(prediction) == prediction.answer.content
        assert prediction.reply == self.sample_reply
        assert prediction.answer == self.sample_answer
