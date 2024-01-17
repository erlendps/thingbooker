from django.conf import settings
from rest_framework import serializers

from thingbooker.things.models import Booking, Rule, Thing


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for booking model"""

    class Meta:
        model = Booking
        fields = ["id", "url", "thing", "booker", "num_people", "status", "start_date", "end_date"]
        read_only_fields = ["status"]


class RuleSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Rule model"""

    class Meta:
        model = Rule
        fields = ["id", "url", "short", "description", "thing"]


class CreateRuleSerializer(serializers.ModelSerializer):
    """Serializer when creating a new rule."""

    class Meta:
        model = Rule
        fields = ["short", "description", "thing"]


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

    def validate_picture(self, value):
        """Validates image is filesize is low enough."""

        filesize = value.size

        if filesize > settings.MEGABYTE_LIMIT * 1024 * 1024:
            raise serializers.ValidationError(
                f"Image is over max file size (>{settings.MEGABYTE_LIMIT * 1024 * 1024})"
            )

        return value
