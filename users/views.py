from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """A class for creating a new user."""

    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Hash password and create user.
        """
        new_user = serializer.save()
        new_user.set_password(new_user.password)
        new_user.save()


class UserDetailView(generics.RetrieveAPIView):
    """A class for returning user data."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the request user.

        :return: The request user.
        """
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        """
        Send a response with basic user data.

        :param request: Default parameter 'request'
        :param args: Default parameter 'args'
        :param kwargs: Default parameter 'kwargs'
        :return: Basic user data.
        """
        user = self.get_queryset()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
