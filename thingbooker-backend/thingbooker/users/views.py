from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from thingbooker.users.permissions import ThingbookerGroupPermission
from thingbooker.users.serializers import ThingbookerGroupSerializer, ThingbookerUserSerializer

if TYPE_CHECKING:
    from django.db.models.query import QuerySet

    from thingbooker.users.models import ThingbookerUser


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides list (/account/) and retrieve (/account/{id}/) methods.
    An authenticated can only list users inside their own group and themselves.
    """

    serializer_class = ThingbookerUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """Fetches a queryset with all users this user is in a group with"""

        user: ThingbookerUser = self.request.user
        return user.get_all_known_users()


class GroupViewSet(viewsets.ModelViewSet):
    """
    Provides list, retrieve, create, update, partial_update and delete methods
    for thingbooker groups.
    """

    serializer_class = ThingbookerGroupSerializer
    permission_classes = [IsAuthenticated, ThingbookerGroupPermission]

    def get_queryset(self) -> QuerySet:
        """Return only the groups the user is related to."""

        user: ThingbookerUser = self.request.user

        return user.thingbooker_groups
