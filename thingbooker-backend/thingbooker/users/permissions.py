from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework import permissions

if TYPE_CHECKING:
    from rest_framework.viewsets import ViewSet

    from thingbooker.base_types import ThingbookerRequest
    from thingbooker.users.models import ThingbookerGroup


class ThingbookerGroupPermission(permissions.BasePermission):
    """Permissions class for thingbooker group."""

    def has_object_permission(
        self, request: ThingbookerRequest, view: ViewSet, obj: ThingbookerGroup
    ) -> bool:
        """
        Checks if user has permissions to do the specified action.
        It assumes the user is authenticated.
        """

        user = request.user

        if user.is_admin_user:
            return True

        if view.action in ["update", "partial_update", "destroy"]:
            return obj.owner == user

        elif view.action in ["retrieve", "invite_member"]:
            return obj.user_is_member(user)

        return True
