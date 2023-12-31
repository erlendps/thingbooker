from uuid import uuid4

from django.contrib.auth.models import Group

from thingbooker.users.models import ThingbookerGroup


class ThingbookerGroupInterface:
    """Interface for thingbooker group."""

    @staticmethod
    def create_auth_group():
        """Creates an auth group with a random name"""

        return Group.objects.create(name=uuid4())

    @classmethod
    def create_with_group(cls, **fields):
        """Creates a thingbooker group with a auth group."""

        group = cls.create_auth_group()
        return ThingbookerGroup.objects.create(group=group, **fields)
