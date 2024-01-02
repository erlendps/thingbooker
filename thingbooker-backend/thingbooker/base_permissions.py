from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import BasePermission

if TYPE_CHECKING:
    from rest_framework.views import APIView

    from thingbooker.base_types import ThingbookerRequest


class IsAdminUser(BasePermission):
    """Custom IsAdminUser permission"""

    def has_permission(self, request: ThingbookerRequest, view: APIView) -> bool:
        """Checks if user is an admin"""

        user = request.user
        return user.is_admin_user
