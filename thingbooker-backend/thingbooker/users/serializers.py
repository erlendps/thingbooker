from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.images import get_image_dimensions
from rest_framework import serializers

from thingbooker.users.interface import ThingbookerGroupInterface
from thingbooker.users.models import AcceptInviteToken, ThingbookerGroup
from thingbooker.utils import hash_token

if TYPE_CHECKING:
    from rest_framework.request import Request

    from thingbooker.users.models import ThingbookerUser


MEGABYTE_LIMIT = 2


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

    thingbooker_groups: serializers.HyperlinkedRelatedField = serializers.HyperlinkedRelatedField(
        "thingbookergroup-detail", many=True, read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = [
            "url",
            "id",
            "username",
            "email",
            "avatar",
            "thingbooker_groups",
            "first_name",
            "last_name",
        ]

    def validate_avatar(self, value):
        """Validates image is squared and filesize is low enough."""

        if not value:
            return value

        filesize = value.size
        width, height = get_image_dimensions(value)

        if width != height:
            raise serializers.ValidationError("Image must be squared.")

        if filesize > MEGABYTE_LIMIT * 1024 * 1024:
            raise serializers.ValidationError(
                f"Image is over max file size (>{MEGABYTE_LIMIT * 1024 * 1024})"
            )

        return value


class ThingbookerShortUserSerializer(serializers.ModelSerializer):
    """Serializer that gives a summary of a user"""

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "avatar", "first_name"]


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for auth.Group"""

    class Meta:
        model = Group
        fields = ["id", "name"]


class ThingbookerGroupSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for thingbooker groups."""

    members: serializers.HyperlinkedRelatedField = serializers.HyperlinkedRelatedField(
        view_name="thingbookeruser-detail", many=True, read_only=True
    )

    class Meta:
        model = ThingbookerGroup
        fields = ["url", "id", "name", "group_picture", "owner", "members"]
        read_only_fields = ["owner"]

    def validate_group_picture(self, value):
        """Validates the size of the group picture."""

        if not value:
            return value

        filesize = value.size

        if filesize > MEGABYTE_LIMIT * 1024 * 1024:
            raise serializers.ValidationError(
                f"Image is over max file size (>{MEGABYTE_LIMIT * 1024 * 1024})"
            )

        return value

    def create(self, validated_data: dict[str, Any]) -> ThingbookerGroup:
        """When creating a thingbooker group, also create the auth.Group instance and link it."""

        owner: ThingbookerUser = self.context.get("request", {"user": None}).user

        return ThingbookerGroupInterface.create_with_group(owner=owner, **validated_data)


class InviteTokenSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer class for AcceptInviteToken model."""

    hashed_token = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = AcceptInviteToken
        fields = [
            "url",
            "group",
            "user",
            "hashed_token",
            "expires_at",
            "used_at",
            "created_at",
            "email",
        ]
        read_only_fields = ["expires_at", "used_at", "created_at", "group", "user"]

    def get_hashed_token(self, obj: AcceptInviteToken):
        """Returns a hashed version of the token"""

        return hash_token(obj.token)
