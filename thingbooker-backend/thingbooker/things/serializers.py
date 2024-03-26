from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from thingbooker.things.enums import BookingStatusEnum
from thingbooker.things.models import Booking, Rule, Thing
from thingbooker.users.serializers import GroupPKField

if TYPE_CHECKING:
    from typing import Any

    from thingbooker.users.models import ThingbookerGroup, ThingbookerUser


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for booking model"""

    class Meta:
        model = Booking
        fields = ["id", "url", "thing", "booker", "num_people", "status", "start_date", "end_date"]
        read_only_fields = ["id", "url", "thing", "booker", "status"]

    def validate(self, data: dict[str, Any]) -> Any:
        """Validates start_date is before end_date"""

        if data["start_date"] >= data["end_date"]:
            raise serializers.ValidationError("End date must be after start date")
        return super().validate(data)


class EditBookingStatusSerializer(serializers.Serializer):
    """Serializer for editing status"""

    new_status = serializers.ChoiceField(choices=BookingStatusEnum.update_choices())
    decline_overlapping = serializers.BooleanField(default=True)

    def create(self, validated_data: Any) -> Any:
        """Returns a tuple of an enum instance and a boolean"""

        return (
            BookingStatusEnum[validated_data["new_status"]],
            validated_data["decline_overlapping"],
        )


class RuleSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Rule model"""

    class Meta:
        model = Rule
        fields = ["id", "url", "short", "description", "thing"]
        read_only_fields = ["id", "url", "thing"]


class ThingSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Thing model"""

    class Meta:
        model = Thing
        fields = [
            "id",
            "url",
            "name",
            "description",
            "picture",
            "owner",
            "members",
            "bookings",
            "rules",
        ]
        read_only_fields = ["id", "url", "owner", "members", "bookings", "rules"]


class CreateThingSerializer(serializers.ModelSerializer):
    """Serializer for creating a thing, has a nested serializer for rules"""

    rules = RuleSerializer(many=True, required=False)

    class Meta:
        model = Thing
        fields = ["name", "description", "picture", "members", "rules"]

    def validate_picture(self, value):
        """Validates image is filesize is low enough."""

        if not value:
            return value
        filesize = value.size

        if filesize > settings.MEGABYTE_LIMIT * 1024 * 1024:
            raise serializers.ValidationError(
                f"Image is over max file size (>{settings.MEGABYTE_LIMIT * 1024 * 1024})"
            )

        return value

    def validate_name(self, value):
        """Validates that the user is not part of a thing with the same name"""

        owner: ThingbookerUser = self.context.get("request", {"user": None}).user
        if owner and owner.things.filter(name=value).exists():
            raise serializers.ValidationError(f"Already part of a group with name: {value}.")

    def create(self, validated_data: Any) -> Thing:
        """Creates the thing along with related rules"""

        rules_data = validated_data.pop("rules", None)

        members = validated_data.pop("members", [])
        owner: ThingbookerUser = validated_data.get("owner", None)

        thing: Thing = Thing.objects.create(**validated_data)

        if owner:
            members.append(owner)
        thing.members.add(*members)

        if rules_data:
            for rule_data in rules_data:
                Rule.objects.create(thing=thing, **rule_data)

        return thing


class AddMembersSerializer(serializers.Serializer):
    """A serializer that can contain either groups or members or both"""

    groups = GroupPKField(many=True, write_only=True)
    users = serializers.ListField(child=serializers.EmailField())

    def create(self, validated_data: serializers.Any) -> tuple[set[ThingbookerUser], set[str]]:
        """
        Concatenates the users in the group with the users list.

        For groups and known users, the users are automatically added. For unknown
        users they are invited.
        """

        user: ThingbookerUser = self.context.get("request", {"user": None}).user

        groups: list[ThingbookerGroup] = validated_data.get("groups", [])
        emails_to_invite: set[str] = set(validated_data.get("users", []))
        users_to_add = set()
        users_to_invite = set()

        if groups:
            auth_groups = [g.group for g in groups]
            users_to_add = set(
                get_user_model().objects.filter(groups__in=auth_groups).distinct("username")
            )

        if user and emails_to_invite:
            qs = user.get_all_known_users().filter(username__in=emails_to_invite)
            users_to_add |= set(qs)
            emails_to_invite -= set(qs.values_list("username", flat=True))
            # sanitize, only invite thingbooker users
            users_to_invite = set(get_user_model().objects.filter(username__in=emails_to_invite))

        return users_to_add, users_to_invite
