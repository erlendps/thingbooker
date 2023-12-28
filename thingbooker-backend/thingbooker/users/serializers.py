from __future__ import annotations

from typing import TYPE_CHECKING

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

if TYPE_CHECKING:
    from rest_framework.request import Request

    from thingbooker.users.models import ThingbookerUser


class ThingbookerRegisterSerializer(RegisterSerializer, serializers.ModelSerializer):
    """Custom register for thingbooker."""

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "avatar",
        )

    def custom_signup(self, request: Request, user: ThingbookerUser):
        """Define custom_signup method to set the additional fields."""

        data = self.validated_data
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        if "avatar" in data:
            user.avatar = data["avatar"]

        user.save()

        return user


class ThingbookerUserSerializer(UserDetailsSerializer, serializers.HyperlinkedModelSerializer):
    """Serializer for thingbooker user."""

    class Meta:
        model = get_user_model()
        fields = ["url", "id", "username", "email", "avatar", "groups"]
