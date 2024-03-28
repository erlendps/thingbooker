from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import BasePermission

from thingbooker.things.models import Thing

if TYPE_CHECKING:
    from typing import Any

    from rest_framework.viewsets import ViewSet

    from thingbooker.base_types import ThingbookerRequest
    from thingbooker.things.models import Booking, Rule


class IsMemberOfThing(BasePermission):
    """Checks the given user is a member of the thing."""

    def has_object_permission(self, request: ThingbookerRequest, view: ViewSet, obj: Any) -> bool:
        """Checks the given user is a member of the thing, and if the action is delete"""

        user = request.user

        if user.is_admin_user:
            return True

        if hasattr(obj, "thing"):
            thing: Thing = obj.thing
            return thing.members.contains(user)
        elif isinstance(obj, Thing):
            return obj.members.contains(user)
        return False


class BookingPermission(BasePermission):
    """Contains permissions specific for Booking"""

    def has_object_permission(
        self, request: ThingbookerRequest, view: ViewSet, obj: Booking
    ) -> bool:
        """Checks for unsafe operations that the user is either owner or booker"""

        user = request.user

        if view.action in ["update", "partial_update", "destroy"]:
            return user == obj.thing.owner or user == obj.booker or user.is_admin_user
        return True


class RulePermission(BasePermission):
    """Contains specific permissions for Rule viewset"""

    def has_object_permission(self, request: ThingbookerRequest, view: ViewSet, obj: Rule) -> bool:
        """Only the owner of the thing can update and destroy"""

        user = request.user

        if view.action in ["update", "partial_update", "destroy"]:
            return user == obj.thing.owner or user.is_admin_user
        return True


class ThingPermission(BasePermission):
    """Contains specific permissions for Thing viewset. Assumes user is member of thing."""

    def has_object_permission(self, request: ThingbookerRequest, view: ViewSet, obj: Thing) -> bool:
        """Only owner can do unsafe actions"""

        user = request.user

        if user.is_admin_user:
            return True

        if view.action in [
            "update",
            "partial_update",
            "destroy",
            "add_rule",
            "update_booking_status",
            "add_members",
            "remove_member",
        ]:
            return obj.owner == user

        return True
