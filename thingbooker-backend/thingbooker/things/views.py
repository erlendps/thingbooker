from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Q
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from thingbooker.things.interface import ThingInterface
from thingbooker.things.models import Booking, Rule, Thing
from thingbooker.things.permissions import (
    BookingPermission,
    IsMemberOfThing,
    RulePermission,
    ThingPermission,
)
from thingbooker.things.serializers import (
    BookingSerializer,
    CreateBookingSerializer,
    CreateRuleSerializer,
    RuleSerializer,
    ThingSerializer,
)

if TYPE_CHECKING:
    from django.db.models.query import QuerySet

    from thingbooker.base_types import ThingbookerRequest
    from thingbooker.users.models import ThingbookerUser


class BookingViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """List, retrieve, update and destroy methods for Booking model"""

    serializer_class = BookingSerializer
    permission_classes = [BookingPermission, IsAuthenticated, IsMemberOfThing]

    def get_queryset(self) -> QuerySet:
        """Fetches the queryset"""

        user: ThingbookerUser = self.request.user

        if user.is_admin_user:
            return Booking.objects.all()

        return Booking.objects.filter(Q(booker=user) | Q(thing__members=user))


class RuleViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """List, retrieve, update and destroy methods for rule model."""

    serializer_class = RuleSerializer
    permission_classes = [IsAuthenticated, IsMemberOfThing, RulePermission]

    def get_queryset(self) -> QuerySet:
        """Fetches the queryset"""

        user: ThingbookerUser = self.request.user

        if user.is_admin_user:
            return Rule.objects.all()
        return Rule.objects.filter(Q(thing__owner=user) | Q(thing__members=user))


class ThingViewSet(viewsets.ModelViewSet):
    """
    Create, list, retrieve, update and destroy methods for thing.

    It also adds some actions, like creating new rules and bookings.
    """

    serializer_class = ThingSerializer
    permission_classes = [IsAuthenticated, IsMemberOfThing, ThingPermission]

    def get_queryset(self) -> QuerySet:
        """Fetches the queryset"""

        user: ThingbookerUser = self.request.user

        if user.is_admin_user:
            return Thing.objects.all()
        return Thing.objects.filter(Q(members=user) | Q(owner=user))

    @action(detail=True, methods=["POST"])
    def add_rule(self, request: ThingbookerRequest, *args, **kwargs):
        """Action for adding a rule to the thing"""

        thing: Thing = self.get_object()

        serializer = CreateRuleSerializer(request.data)

        if serializer.is_valid():
            rule: Rule = serializer.save(thing=thing)
            return Response(data=RuleSerializer(rule).data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"])
    def add_booking(self, request: ThingbookerRequest, *args, **kwargs):
        """Action for adding a new booking to the thing."""

        thing: Thing = self.get_object()

        serializer = CreateBookingSerializer(request.data)

        if serializer.is_valid():
            response = ThingInterface.add_new_booking(
                thing=thing, user=request.user, serializer=serializer
            )

            if 200 <= response.code < 300:
                return Response(
                    data=BookingSerializer(response.payload).data, status=status.HTTP_201_CREATED
                )
            serializer.errors.update(response.payload)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
