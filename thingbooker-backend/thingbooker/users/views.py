from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from thingbooker.base_permissions import IsAdminUser
from thingbooker.things.interface import ThingInterface
from thingbooker.users.enums import MembershipStatusEnum
from thingbooker.users.interface import ThingbookerGroupInterface
from thingbooker.users.models import AcceptGroupInviteToken, AcceptThingInviteToken, ThingbookerUser
from thingbooker.users.permissions import ThingbookerGroupPermission
from thingbooker.users.serializers import (
    GroupInviteTokenSerializer,
    RemoveMemberSerializer,
    ThingbookerGroupSerializer,
    ThingbookerShortUserSerializer,
    ThingbookerUserSerializer,
    ThingInviteTokenSerializer,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from uuid import UUID

    from django.db.models.query import QuerySet

    from thingbooker.base_types import ThingbookerRequest, ThingbookerResponse
    from thingbooker.users.models import ThingbookerGroup


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides list (/account/) and retrieve (/account/{id}/) methods.
    An authenticated can only list users inside their own group and themselves.
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Returns the short serializer if 'short' query param is given."""

        if self.request.query_params.get("short", None) == "true":
            return ThingbookerShortUserSerializer
        return ThingbookerUserSerializer

    def get_queryset(self) -> QuerySet:
        """Fetches a queryset with all users this user is in a group with"""

        user: ThingbookerUser = self.request.user

        # check if user is admin
        if user.is_admin_user:
            return get_user_model().objects.all()
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

    @action(detail=True, methods=["POST"], url_path="invite-member/")
    def invite_member(self, request: ThingbookerRequest, pk: UUID | None = None, format=None):
        """Invites one or more members to a group."""

        user = request.user
        group: ThingbookerGroup = self.get_object()
        serializer = GroupInviteTokenSerializer(data=request.data)
        if serializer.is_valid():
            email: str = serializer.validated_data.get("email")
            if not email:
                return Response(
                    {"message": "No email supplied"}, status=status.HTTP_400_BAD_REQUEST
                )
            invite_successful_msg = {
                "message": "The user has been invited if they are registered on thingbooker"
            }

            invited_user: ThingbookerUser = ThingbookerUser.objects.get_or_none(username=email)
            if not invited_user:
                # give a generic response so that a user cannot spam the endpoint to check
                # which users exists
                return Response(invite_successful_msg, status=status.HTTP_200_OK)

            result = ThingbookerGroupInterface.invite_user_to_group(invited_user, group, user)
            if result == MembershipStatusEnum.MEMBER:
                msg = {"message": "User is already a member of the group"}
            elif result == MembershipStatusEnum.ALREADY_INVITED:
                msg = {"message": "User is already invited to the group"}
            else:
                msg = invite_successful_msg

            return Response(msg, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"], url_path="remove-member")
    def remove_member(self, request: ThingbookerRequest):
        """Removes the user (if a membership exists) from the group."""

        group: ThingbookerGroup = self.get_object()
        serializer = RemoveMemberSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_to_remove = serializer.save()
        if not group.members.contains(user_to_remove):
            return Response(
                data={"error": "User is not member of group"}, status=status.HTTP_409_CONFLICT
            )

        group.members.remove(user_to_remove)
        return Response(data={"message": "User removed from group"}, status=status.HTTP_200_OK)


class InviteTokenViewSet(viewsets.ReadOnlyModelViewSet):
    """A generic viewset for Invite Tokens. The viewset should ONLY be inherited, not used"""

    serializer_class = None
    permission_classes = [IsAuthenticated, IsAdminUser]
    klass: AcceptGroupInviteToken | AcceptThingInviteToken = None
    accept_function: Callable[[str], ThingbookerResponse] = None
    queryset = None

    @action(
        methods=["POST"],
        detail=False,
        url_path="accept-invite/(?P<token>.+)",
        permission_classes=[IsAuthenticated],
    )
    def accept_invite(self, request: ThingbookerRequest, token: str):
        """Accepts a invite to a group"""

        if self.klass is None or self.accept_function is None:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

        user = request.user
        invite_token = self.klass.objects.get_or_none(user=user, token=token)

        if not invite_token:
            return Response(status=status.HTTP_404_NOT_FOUND)

        payload = self.accept_function(invite_token)

        return Response(data=payload, status=status.HTTP_200_OK)


class GroupInviteTokenViewSet(InviteTokenViewSet):
    """Provides list and retrieve actions for AcceptInviteToken model."""

    serializer_class = GroupInviteTokenSerializer
    queryset = AcceptGroupInviteToken.objects.all()
    klass = AcceptGroupInviteToken
    accept_function = ThingbookerGroupInterface.accept_group_invite


class ThingInviteTokenViewSet(InviteTokenViewSet):
    """Provides list and retrieve actions for AcceptInviteToken model."""

    serializer_class = ThingInviteTokenSerializer
    queryset = AcceptThingInviteToken.objects.all()
    klass = AcceptThingInviteToken
    accept_function = ThingInterface.accept_thing_invite
