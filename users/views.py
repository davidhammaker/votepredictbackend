from rest_framework import generics

from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Hash password and create user.
        """
        new_user = serializer.save()
        new_user.set_password(new_user.password)
        new_user.save()
