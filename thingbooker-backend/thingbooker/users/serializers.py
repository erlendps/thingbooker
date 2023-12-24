from django.contrib.auth import get_user_model
from rest_framework import serializers


class ThingbookerSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for thingbooker user."""

    class Meta:
        model = get_user_model()
        fields = ["url", "id", "username", "email", "avatar", "groups"]
