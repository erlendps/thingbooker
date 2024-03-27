from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from django.contrib.auth.models import Group
from django.utils import timezone

from thingbooker.base_types import ThingbookerResponse
from thingbooker.mail.interface import EmailInterface
from thingbooker.users.enums import InviteStatusEnum, MembershipStatusEnum
from thingbooker.users.models import AcceptGroupInviteToken, ThingbookerGroup

if TYPE_CHECKING:
    from thingbooker.users.models import ThingbookerUser


class ThingbookerGroupInterface:
    """Interface for thingbooker group."""

    DEFAULT_INVITE_SUBJECT = "[Thingbooker] Du har blitt invitert til en gruppe!"

    @staticmethod
    def create_auth_group():
        """Creates an auth group with a random name"""

        return Group.objects.create(name=uuid4())

    @classmethod
    def create_with_group(cls, **fields):
        """Creates a thingbooker group with a auth group."""

        group = cls.create_auth_group()
        owner = fields.get("owner")
        tb_group = ThingbookerGroup.objects.create(group=group, **fields)
        tb_group.members.add(owner)
        return tb_group

    @classmethod
    def invite_user_to_group(
        cls, user: ThingbookerUser, group: ThingbookerGroup, inviter: ThingbookerUser
    ) -> MembershipStatusEnum:
        """Method for inviting a user to a group. Sends an email with a activation link."""

        if group.user_is_member(user):
            return MembershipStatusEnum.MEMBER

        elif AcceptGroupInviteToken.objects.get_or_none(
            user=user, group=group, expires_at__gt=timezone.now()
        ):
            return MembershipStatusEnum.ALREADY_INVITED

        invite_token: AcceptGroupInviteToken = AcceptGroupInviteToken.objects.create(
            user=user, group=group
        )
        context = {"token": invite_token, "group": group, "invited_by": inviter, "user": user}
        EmailInterface.send_mail(
            template_name="users/invite_user_to_group",
            context=context,
            to_address=user.username,
            subject=cls.DEFAULT_INVITE_SUBJECT,
        )
        return MembershipStatusEnum.SENT_INVITE

    @classmethod
    def accept_group_invite(cls, token: AcceptGroupInviteToken) -> ThingbookerResponse:
        """Method for accepting a group invite. Will add the user to the group."""

        if token.is_expired:
            message = InviteStatusEnum.TOKEN_EXPIRED
        elif token.is_used:
            message = InviteStatusEnum.TOKEN_USED
        else:
            message = InviteStatusEnum.TOKEN_CONSUMED

        # add user to group
        group = token.group
        group.members.add(token.user)

        # set token as used
        token.used_at = timezone.now()
        token.save()

        payload = {"message": message}

        return ThingbookerResponse(code=200, payload=payload)
