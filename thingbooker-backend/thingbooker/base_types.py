from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.request import Request

if TYPE_CHECKING:
    from typing import Any

    from thingbooker.users.models import ThingbookerUser


class ThingbookerRequest(Request):
    """Adds correct typechecking for the user field."""

    user: ThingbookerUser


class ThingbookerResponse:
    """Simple response type used internally."""

    def __init__(self, code: int, payload: Any) -> None:
        self.code = code
        self.payload = payload
