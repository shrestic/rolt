from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rolt.core.exceptions import ApplicationError


class UserCreateSerializer(BaseUserCreateSerializer):
    re_password = serializers.CharField(write_only=True, required=True)
    is_staff = serializers.BooleanField(default=False, required=False)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "re_password",
            "is_staff",
        ]

    def validate(self, attrs):
        password = attrs.get("password")
        re_password = attrs.get("re_password")

        if password and re_password and password != re_password:
            raise ApplicationError(message="Passwords do not match.")
        if attrs.get("is_staff"):
            request = self.context.get("request")
            if not (
                request and request.user.is_authenticated and request.user.is_superuser
            ):
                msg = "Only superusers can create staff users."
                raise ApplicationError(msg)

        return attrs

    def create(self, validated_data):
        validated_data.pop("re_password", None)
        first_name = validated_data.pop("first_name", "")
        last_name = validated_data.pop("last_name", "")
        is_staff = validated_data.get("is_staff", False)
        validated_data["is_staff"] = is_staff
        user = super().create(validated_data)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ["username", "email", "first_name", "last_name"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_staff"] = user.is_staff
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["is_staff"] = self.user.is_staff
        data["groups"] = list(self.user.groups.values_list("name", flat=True))
        return data
