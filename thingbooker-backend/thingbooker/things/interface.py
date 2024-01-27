from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Q
from django.utils import timezone

from thingbooker.base_types import ThingbookerResponse
from thingbooker.things.enums import BookingStatusEnum

if TYPE_CHECKING:
    from datetime import datetime

    from thingbooker.things.models import Booking, Thing
    from thingbooker.things.serializers import BookingSerializer
    from thingbooker.users.models import ThingbookerUser


class ThingInterface:
    """Helper methods relating to things."""

    @staticmethod
    def get_overlapping_bookings(
        thing: Thing, booking: Booking = None, start: datetime = None, end: datetime = None
    ):
        """Finds and returns bookings that overlap with the given status query."""

        if booking:
            start = booking.start_date
            end = booking.end_date

        if not (start and end):
            return thing.bookings.none()

        bookings = thing.bookings.filter(start_date__lte=end, end_date__gte=start)

        if booking:
            bookings = bookings.exclude(pk=booking.pk)

        return bookings

    @classmethod
    def add_new_booking(cls, thing: Thing, user: ThingbookerUser, serializer: BookingSerializer):
        """Tries creating a new booking on the given dates, returns either an error dictionary, or
        the created booking.

        Assumes the serializer is valid.
        """

        start: datetime = serializer.validated_data["start_date"]
        end: datetime = serializer.validated_data["end_date"]
        bookings = cls.get_overlapping_bookings(thing, start=start, end=end)
        bookings = bookings.filter(
            Q(start_date__gte=timezone.now()) & Q(status=BookingStatusEnum.ACCEPTED.value)
        )

        if bookings.exists():
            overlapping_booking = bookings.first()
            payload = {}
            if overlapping_booking.start_date <= end and overlapping_booking.end_date >= end:
                payload.update({"end_date": "Cannot end booking after another starts."})
            if overlapping_booking.end_date >= start and overlapping_booking.start_date <= start:
                payload.update({"start_date": "Cannot start booking before another ends."})

            return ThingbookerResponse(code=400, payload=payload)

        booking = serializer.save(thing=thing, booker=user)

        return ThingbookerResponse(code=201, payload=booking)

    @classmethod
    def accept_booking(cls, thing: Thing, booking: Booking, decline_overlapping: bool = True):
        """Accepts a booking, and declines all other bookings that overlap."""

        bookings = cls.get_overlapping_bookings(thing, booking=booking)
        if bookings.filter(status=BookingStatusEnum.ACCEPTED.value).exists():
            return ThingbookerResponse(
                code=409,
                payload={"error": "There is already an accepted booking in this time frame"},
            )

        booking.status = BookingStatusEnum.ACCEPTED
        booking.save()
        payload = {"accepted": "Booking was accepted"}
        if decline_overlapping:
            declined = bookings.update(status=BookingStatusEnum.DECLINED)
            payload.update({"num_declined": declined})

        return ThingbookerResponse(code=200, payload=payload)
