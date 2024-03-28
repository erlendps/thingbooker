from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from django.db.models import Q
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from thingbooker.things.enums import BookingStatusEnum
from thingbooker.things.interface import ThingInterface
from thingbooker.things.models import Booking, Rule, Thing
from thingbooker.things.permissions import (
    BookingPermission,
    IsMemberOfThing,
    RulePermission,
    ThingPermission,
)
from thingbooker.things.serializers import (
    AddMembersSerializer,
    BookingSerializer,
    CreateThingSerializer,
    EditBookingStatusSerializer,
    RuleSerializer,
    ThingSerializer,
)
from thingbooker.users.serializers import RemoveMemberSerializer

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

    permission_classes = [IsAuthenticated, IsMemberOfThing, ThingPermission]

    def get_queryset(self) -> QuerySet:
        """Fetches the queryset"""

        user: ThingbookerUser = self.request.user

        if user.is_admin_user:
            return Thing.objects.all()
        return Thing.objects.filter(Q(members=user) | Q(owner=user))

    def get_serializer_class(self):
        """Returns specific serializer for create action"""

        if self.action == "create":
            return CreateThingSerializer
        elif self.action == "add_rule":
            return RuleSerializer
        elif self.action == "add_booking":
            return BookingSerializer
        elif self.action == "add_members":
            return AddMembersSerializer
        return ThingSerializer

    def perform_create(self, serializer: CreateThingSerializer) -> None:
        """Creates the thing along with related rules"""

        user = self.request.user
        serializer.save(owner=user)

    @action(detail=True, methods=["POST"], url_path="add-rule/")
    def add_rule(self, request: ThingbookerRequest, *args, **kwargs):
        """Action for adding a rule to the thing"""

        thing: Thing = self.get_object()

        serializer: RuleSerializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            rule: Rule = serializer.save(thing=thing)
            return Response(data=self.get_serializer(rule).data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"], url_path="add-booking/")
    def add_booking(self, request: ThingbookerRequest, *args, **kwargs):
        """Action for adding a new booking to the thing."""

        thing: Thing = self.get_object()

        serializer: BookingSerializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            response = ThingInterface.add_new_booking(
                thing=thing, user=request.user, serializer=serializer
            )

            if 200 <= response.code < 300:
                return Response(
                    data=self.get_serializer(response.payload).data, status=status.HTTP_201_CREATED
                )
            return Response(data=response.payload, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"], url_path="update-booking-status/(?P<booking_id>.+)")
    def update_booking_status(self, request: ThingbookerRequest, booking_id: str):
        """Action for updating the booking status."""

        thing: Thing = self.get_object()
        try:
            booking = thing.bookings.get(pk=uuid.UUID(booking_id))
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EditBookingStatusSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        action, decline_overlapping = serializer.save()

        if action == BookingStatusEnum.ACCEPTED:
            response = ThingInterface.accept_booking(thing, booking, decline_overlapping)
            return Response(data=response.payload, status=response.code)

        booking.status = BookingStatusEnum.DECLINED
        booking.save()
        return Response(data={"declined": "Booking was declined"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path="all-rules")
    def all_rules(self):
        """Fetches all rules for the thing"""

        thing: Thing = self.get_object()

        serializer = RuleSerializer(instance=thing.rules.all(), many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path="all-bookings")
    def all_bookings(self):
        """Fetches all bookings (waiting or accepted) for the thing"""

        thing: Thing = self.get_object()
        bookings = thing.bookings.exclude(status=BookingStatusEnum.DECLINED.value)

        serializer = BookingSerializer(instance=bookings, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="add-members")
    def add_members(self, request: ThingbookerRequest):
        """Adds users to the thing"""

        thing: Thing = self.get_object()
        serializer = AddMembersSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        users_to_add: set[ThingbookerUser]
        users_to_invite: set[ThingbookerUser]
        users_to_add, users_to_invite = serializer.save()

        thing.members.add(*users_to_add)

        data = {"users_added": [str(u.id) for u in users_to_add]}

        payload = ThingInterface.invite_users_to_thing(thing=thing, users_to_invite=users_to_invite)
        data.update(payload)

        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="remove-member")
    def remove_member(self, request: ThingbookerRequest):
        """Removes a member from the thing (if they are a member)"""

        thing: Thing = self.get_object()
        serializer = RemoveMemberSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_to_remove: ThingbookerUser = serializer.save()

        if not thing.members.contains(user_to_remove):
            return Response(
                data={"error": "User is not part of this group"}, status=status.HTTP_409_CONFLICT
            )
        thing.members.remove(user_to_remove)
        return Response(data={"message": "User was removed"}, status=status.HTTP_200_OK)
