from django.contrib.auth import get_user_model
from rest_framework import serializers

from .validators import me_username_validator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)  # type:ignore


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(
        max_length=150, validators=(me_username_validator,)
    )


class UserTokenObtainingSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=16)
