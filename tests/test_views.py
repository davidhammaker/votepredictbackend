from unittest import mock

import pytz
from django.utils import timezone
from rest_framework.test import APITestCase, APIRequestFactory

from votepredictapp.models import Answer, Prediction, Question, Reply, Vote
from votepredictapp.views import QuestionViewSet


def utc_date(year: int, month: int, day: int):
    return timezone.datetime(year, month, day, tzinfo=pytz.utc)


class TestViews(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        Question.objects.create(
            content="open question",
            start_date=utc_date(2021, 8, 1),
            end_date=utc_date(2021, 8, 31),
        )
        Question.objects.create(
            content="closed question",
            start_date=utc_date(2021, 7, 1),
            end_date=utc_date(2021, 7, 31),
        )
        Question.objects.create(
            content="future question",
            start_date=utc_date(2021, 9, 1),
            end_date=utc_date(2021, 9, 30),
        )
        self.today = utc_date(2021, 8, 23)

    @mock.patch("votepredictapp.models.timezone")
    def test_questions_view(self, mock_timezone):
        mock_timezone.datetime.now.return_value = self.today
        request = self.factory.get("")  # Empty string; info in actions
        response = QuestionViewSet.as_view(actions={"get": "list"})(request)
        assert len(response.data) == 1
        assert response.data[0]["content"] == "open question"

    @mock.patch("votepredictapp.models.timezone")
    def test_closed_questions(self, mock_timezone):
        mock_timezone.datetime.now.return_value = self.today
        request = self.factory.get("")
        response = QuestionViewSet.as_view(actions={"get": "closed"})(request)
        assert len(response.data) == 1
        assert response.data[0]["content"] == "closed question"
