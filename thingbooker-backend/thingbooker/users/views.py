from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from thingbooker.users.serializers import ThingbookerUserSerializer

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
        qs = get_user_model().objects.filter(pk=user.id)

        for g in user.groups.all():
            qs = qs.union(g.user_set.all())

        return qs
