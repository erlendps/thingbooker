from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.request import Request

if TYPE_CHECKING:
    from thingbooker.users.models import ThingbookerUser


class ThingbookerRequest(Request):
    """Adds correct typechecking for the user field."""

    user: ThingbookerUser
