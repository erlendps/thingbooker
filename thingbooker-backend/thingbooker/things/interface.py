from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Q
from django.utils import timezone

from thingbooker.base_types import ThingbookerResponse
from thingbooker.things.enums import BookingStatusEnum

if TYPE_CHECKING:
    from datetime import datetime

    from thingbooker.things.models import Thing
    from thingbooker.things.serializers import CreateBookingSerializer
    from thingbooker.users.models import ThingbookerUser


class ThingInterface:
    """Helper methods relating to things."""

    @staticmethod
    def add_new_booking(thing: Thing, user: ThingbookerUser, serializer: CreateBookingSerializer):
        """Tries creating a new booking on the given dates, returns either an error dictionary, or
        the created booking.

        Assumes the serializer is valid.
        """

        start: datetime = serializer.validated_data["start_date"]
        end: datetime = serializer.validated_data["end_date"]
        bookings = thing.bookings.filter(
            Q(start_date__gte=timezone.now()) & ~Q(status=BookingStatusEnum.ACCEPTED.value)
        )

        if (bookings := bookings.filter(start_date__lte=start, end_date__gte=end)).exists():
            overlapping_booking = bookings.first()
            payload = {}
            if overlapping_booking.start_date <= end:
                payload.update({"end_date": "Cannot end booking after another starts."})
            if overlapping_booking.end_date >= start:
                payload.update({"start_date": "Cannot start booking before another ends."})

            return ThingbookerResponse(code=400, payload=payload)

        booking = serializer.save(thing=thing, booker=user)

        return ThingbookerResponse(code=201, payload=booking)
