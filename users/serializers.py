from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that email address already exists.",
            )
        ],
    )
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields = ["id", "username", "email", "password"]
        model = User
