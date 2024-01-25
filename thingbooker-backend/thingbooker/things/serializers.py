from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from rest_framework import serializers

from thingbooker.things.models import Booking, Rule, Thing

if TYPE_CHECKING:
    from typing import Any


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

    def create(self, validated_data: Any) -> Thing:
        """Creates the thing along with related rules"""

        rules_data = validated_data.pop("rules", None)

        members = validated_data.pop("members", None)
        owner = validated_data.get("owner", None)

        thing: Thing = Thing.objects.create(**validated_data)

        if members:
            if owner:
                members.append(owner)
            thing.members.add(*members)

        if rules_data:
            for rule_data in rules_data:
                Rule.objects.create(thing=thing, **rule_data)

        return thing
