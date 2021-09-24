from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from users.views import CreateUserView, UserDetailView


class TestUsersViews(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.sample_user = User.objects.create_user(
            "sample_username",
            "sample_email",
            "sample_password",
        )

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
        assert User.objects.get(username="user123").email == "user123@example.com"

    def test_login(self):
        User.objects.create_user("user456", "user456@example.com", "5678")
        response = self.client.post(
            "/api-token-auth/", {"username": "user456", "password": "5678"}
        )
        assert response.status_code == 200
        assert set(response.data.keys()) == {"token"}

    def test_get_user(self):
        request = self.factory.get("/get-user/")
        force_authenticate(request, self.sample_user)
        response = UserDetailView.as_view()(request)
        assert response.status_code == 200
        assert response.data == {
            "id": 1,
            "username": "sample_username",
            "email": "sample_email",
        }
