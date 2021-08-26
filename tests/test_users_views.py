from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase

from users.views import CreateUserView


class TestUsersViews(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_create_user(self):
        request = self.factory.post(
            "/create-user/",
            {
                "username": "user123",
                "email": "user123@example.com",
                "password": "1234",
            },
        )
        response = CreateUserView.as_view()(request)
        assert response.status_code == 201
        assert set(response.data.keys()) == {"id", "username", "email"}
        assert User.objects.first().username == "user123"

    def test_login(self):
        User.objects.create_user("user456", "user456@example.com", "5678")
        response = self.client.post(
            "/api-token-auth/", {"username": "user456", "password": "5678"}
        )
        assert response.status_code == 200
        assert set(response.data.keys()) == {"token"}
