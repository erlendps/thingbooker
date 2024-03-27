from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from thingbooker.base_types import ThingbookerResponse
from thingbooker.mail.interface import EmailInterface
from thingbooker.things.enums import BookingStatusEnum
from thingbooker.users.enums import InviteStatusEnum, MembershipStatusEnum
from thingbooker.users.models import AcceptThingInviteToken

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import datetime

    from thingbooker.things.models import Booking, Thing
    from thingbooker.things.serializers import BookingSerializer
    from thingbooker.things.types import ThingInviteDict
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

        url = f"{settings.CLIENT_BASE_URL}things/{thing.name}/"
        context = {"booking": booking, "thing": thing, "update_status_url": url}
        EmailInterface.send_mail(
            template_name="things/notify_owner_of_new_booking",
            context=context,
            to_address=thing.owner.username,
            subject="[Thingbooker] Ny booking",
        )

        return ThingbookerResponse(code=201, payload=booking)

    @classmethod
    def accept_booking(cls, thing: Thing, booking: Booking, decline_overlapping: bool = True):
        """Accepts a booking, and declines all other bookings that overlap."""

        bookings = cls.get_overlapping_bookings(thing, booking=booking).select_related(
            "thing", "booker"
        )
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

            for b in bookings:
                if b.booker == thing.owner:
                    continue
                context = {"declined": True, "booking": b}
                EmailInterface.send_mail(
                    template_name="things/notify_booking_status_changed",
                    context=context,
                    to_address=b.booker.username,
                    subject="[Thingbooker] Bookingen din er avvist",
                )

        if booking.booker != thing.owner:
            context = {"declined": False, "booking": booking}
            EmailInterface.send_mail(
                template_name="things/notify_booking_status_changed",
                context=context,
                to_address=booking.booker.username,
                subject="[Thingbooker] Bookingen din er godtatt",
            )

        return ThingbookerResponse(code=200, payload=payload)

    @classmethod
    def invite_users_to_thing(cls, thing: Thing, users_to_invite: Iterable[ThingbookerUser]):
        """Invites the users in user_emails"""

        payload: dict[str, list[ThingInviteDict]] = {"users_invited": []}
        for user in users_to_invite:
            if thing.user_is_member(user):
                payload["users_invited"].append(
                    {"id": str(user.id), "status": MembershipStatusEnum.MEMBER}
                )
                continue

            elif AcceptThingInviteToken.objects.get_or_none(
                user=user, thing=thing, expires_at__gt=timezone.now()
            ):
                payload["users_invited"].append(
                    {"id": str(user.id), "status": MembershipStatusEnum.ALREADY_INVITED}
                )
                continue

            invite_token: AcceptThingInviteToken = AcceptThingInviteToken.objects.create(
                user=user, thing=thing
            )
            context = {"token": invite_token, "thing": thing, "user": user}
            EmailInterface.send_mail(
                template_name="things/invite_user_to_thing",
                context=context,
                to_address=user.username,
                subject="[Thingbooker] Du har blitt invitert til en ting!",
            )
            payload["users_invited"].append(
                {"id": str(user.id), "status": MembershipStatusEnum.SENT_INVITE}
            )
        return ThingbookerResponse(code=200, payload=payload)

    @classmethod
    def accept_thing_invite(token: AcceptThingInviteToken):
        """Method for handling the user accepting an invite to a thing."""

        if token.is_expired:
            message = InviteStatusEnum.TOKEN_EXPIRED
        elif token.is_used:
            message = InviteStatusEnum.TOKEN_USED
        else:
            message = InviteStatusEnum.TOKEN_CONSUMED

        payload = {"message": message}

        thing = token.thing
        thing.members.add(token.user)

        token.used_at = timezone.now()
        token.save()

        return ThingbookerResponse(code=200, payload=payload)
