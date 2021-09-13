from unittest import mock

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from votepredictapp.models import Answer, Prediction, Question, Reply, Vote
from votepredictapp.views import ReplyView, TotalsView


class TestViews(APITestCase):
    def setUp(self) -> None:
        # Request factory
        self.factory = APIRequestFactory()

        # Questions with dates
        self.today = timezone.now()
        self.open_question = Question.objects.create(
            content="open question",
            start_date=self.today - timezone.timedelta(days=7),
            end_date=self.today + timezone.timedelta(days=7),
        )
        self.closed_question = Question.objects.create(
            content="closed question",
            start_date=self.today - timezone.timedelta(days=14),
            end_date=self.today - timezone.timedelta(days=7),
        )
        self.future_question = Question.objects.create(
            content="future question",
            start_date=self.today + timezone.timedelta(days=7),
            end_date=self.today + timezone.timedelta(days=14),
        )

        # Answers
        Answer.objects.create(content="answer 1", question=self.closed_question)
        Answer.objects.create(content="answer 2", question=self.closed_question)
        Answer.objects.create(content="answer 3", question=self.open_question)
        Answer.objects.create(content="answer 4", question=self.open_question)

        # Users
        self.user_1 = User.objects.create_user("user 1")
        self.user_2 = User.objects.create_user("user 2")

        # Replies
        self.reply_1 = Reply.objects.create(
            question=self.closed_question, user=self.user_1
        )
        self.reply_2 = Reply.objects.create(
            question=self.open_question, user=self.user_1
        )

        # Votes and Prediction
        Vote.objects.create(
            reply=self.reply_1, answer=self.closed_question.answers.all()[0]
        )
        Prediction.objects.create(
            reply=self.reply_1, answer=self.closed_question.answers.all()[1]
        )
        Vote.objects.create(
            reply=self.reply_2, answer=self.closed_question.answers.all()[1]
        )
        Prediction.objects.create(
            reply=self.reply_2, answer=self.closed_question.answers.all()[0]
        )

    @mock.patch("votepredictapp.models.timezone")
    def test_questions_list_view(self, mock_timezone):
        mock_timezone.now.return_value = self.today
        response = self.client.get("/questions/")
        assert len(response.data) == 1
        assert response.data[0]["content"] == "open question"

    @mock.patch("votepredictapp.models.timezone")
    def test_closed_questions(self, mock_timezone):
        mock_timezone.now.return_value = self.today
        response = self.client.get("/questions/closed/")
        assert len(response.data) == 1
        assert response.data[0]["content"] == "closed question"

    @mock.patch("votepredictapp.models.timezone")
    def test_questions_detail_view(self, mock_timezone):
        mock_timezone.now.return_value = self.today
        response = self.client.get("/questions/1/")
        assert response.data["content"] == "open question"

    def test_reply_view_unauthorized(self):
        response = self.client.get("/reply/")
        assert response.status_code == 401

    def test_reply_view(self):
        request = self.factory.get("/reply/")
        force_authenticate(request, self.user_1)
        response = ReplyView.as_view()(request)
        assert response.status_code == 200
        assert len(response.data) == 2
        assert set(response.data[0].keys()) == {"id", "question", "vote", "prediction"}
        assert set(response.data[0]["question"].keys()) == {"id"}

    def test_reply_view_no_replies(self):
        request = self.factory.get("/reply/")
        force_authenticate(request, self.user_2)
        response = ReplyView.as_view()(request)
        assert response.status_code == 200
        assert response.data == []

    def test_create_reply(self):
        request = self.factory.post(
            "/reply/",
            data={
                "question_id": self.open_question.id,
                "vote_id": self.open_question.answers.all()[0].id,
                "prediction_id": self.open_question.answers.all()[0].id,
            },
        )
        force_authenticate(request, self.user_2)
        response = ReplyView.as_view()(request)
        assert response.status_code == 201
        assert set(response.data.keys()) == {"id", "question", "vote", "prediction"}
        assert set(response.data["question"].keys()) == {"id", "content", "answers"}

    def test_create_reply_post_body_error(self):
        request = self.factory.post("/reply/", data={})
        force_authenticate(request, self.user_2)
        response = ReplyView.as_view()(request)
        assert response.status_code == 400
        assert set(response.data["detail"].keys()) == {
            "question_id",
            "vote_id",
            "prediction_id",
        }

    def test_create_reply_missing_question_error(self):
        request = self.factory.post(
            "/reply/",
            data={
                "question_id": self.future_question.id,
                "vote_id": self.open_question.answers.first().id,
                "prediction_id": self.open_question.answers.first().id,
            },
        )
        force_authenticate(request, self.user_2)
        response = ReplyView.as_view()(request)
        assert response.status_code == 400
        assert (
            str(response.data["detail"])
            == f"Question {self.future_question.id} is not active or does not exist"
        )

    def test_create_reply_invalid_answer_error(self):
        request = self.factory.post(
            "/reply/",
            data={
                "question_id": self.open_question.id,
                "vote_id": self.closed_question.answers.first().id,
                "prediction_id": self.closed_question.answers.first().id,
            },
        )
        force_authenticate(request, self.user_2)
        response = ReplyView.as_view()(request)
        assert response.status_code == 400
        assert (
            str(response.data["detail"])
            == f"Answers must be one of the following for question "
            f"{self.open_question.id}: "
            f"{[answer.id for answer in self.open_question.answers.all()]}"
        )

    def test_replace_reply(self):
        request = self.factory.post(
            "/reply/",
            data={
                "question_id": self.open_question.id,
                "vote_id": self.open_question.answers.first().id,
                "prediction_id": self.open_question.answers.first().id,
            },
        )
        force_authenticate(request, self.user_1)
        response = ReplyView.as_view()(request)
        assert response.status_code == 201
        assert response.data["vote"]["answer"] == self.open_question.answers.first().id
        assert (
            response.data["prediction"]["answer"]
            == self.open_question.answers.first().id
        )

    def test_totals_list_view(self):
        request = self.factory.get("/totals/")
        force_authenticate(request, self.user_1)
        response = TotalsView.as_view()(request)
        assert response.status_code == 200
        assert set(response.data.keys()) == {"questions", "correct_predictions"}
        assert set(response.data["questions"][0].keys()) == {
            "id",
            "content",
            "answers",
            "totals",
            "vote",
            "prediction",
            "correct_prediction",
        }

    def test_totals_list_view_unanswered(self):
        request = self.factory.get("/totals/")
        force_authenticate(request, self.user_2)
        response = TotalsView.as_view()(request)
        assert response.status_code == 200
        assert set(response.data.keys()) == {"questions", "correct_predictions"}
        assert set(response.data["questions"][0].keys()) == {
            "id",
            "content",
            "answers",
            "totals",
        }
