from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from thingbooker.users.enums import MembershipStatusEnum


class ThingInviteDict(TypedDict):
    """A typed dict for a ThingInvite used in ThingInterface.invite_users_to_thing"""

    id: str
    status: MembershipStatusEnum
