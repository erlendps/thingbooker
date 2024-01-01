from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from thingbooker.users.models import ThingbookerGroup
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
        return get_user_model().objects.filter(id__in=user.get_all_known_user_ids())


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

        tb_group_ids = user.groups.all().values_list("thingbooker_group", flat=True)
        return ThingbookerGroup.objects.filter(id__in=tb_group_ids)
