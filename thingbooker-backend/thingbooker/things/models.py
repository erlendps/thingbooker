from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, validate_image_file_extension
from django.db import models
from django.utils import timezone

from thingbooker.base_models import ThingbookerManager, ThingbookerModel
from thingbooker.things.enums import BookingStatusEnum

if TYPE_CHECKING:
    from django.db.models.manager import ManyToManyRelatedManager, RelatedManager

    from thingbooker.users.models import ThingbookerUser


def thing_picture_upload_path(instance: Thing, filename: str):
    """Returns the path to upload thing pictures to."""

    extension = filename.split(".")[-1]

    return f"things/pictures/{instance.id}.{extension}"


class Thing(ThingbookerModel):
    """
    Model for a thing.

    A thing is something that can be booked. A think has a collection of members
    which is derived from the group which is connected to it.
    """

    if TYPE_CHECKING:
        bookings: RelatedManager[Booking]
        rules: RelatedManager[Rule]

    name = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)
    picture = models.ImageField(
        upload_to=thing_picture_upload_path,
        null=True,
        blank=True,
        validators=[validate_image_file_extension],
    )

    owner: ThingbookerUser = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="owned_things"
    )
    members: ManyToManyRelatedManager[ThingbookerUser] = models.ManyToManyField(
        get_user_model(), related_name="things"
    )

    objects: ThingbookerManager = ThingbookerManager()

    class Meta:
        permissions = [("can_manage_booking", "User can manage (accept/decline) booking")]

    def user_is_member(self, user: ThingbookerUser):
        """Returns true if the user is a member."""

        return self.members.contains(user)

    def __str__(self) -> str:
        return f"{self.name} with owner {self.owner}"


class Booking(ThingbookerModel):
    """
    Model for a booking.

    A booking firstly indicates if it is approved or declined. It also contains
    meta information about the booking, such as time-frame, number of people and so on.
    """

    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name="bookings")

    booker: ThingbookerUser = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="bookings"
    )

    num_people = models.PositiveIntegerField(
        verbose_name="Number of guests using the thing",
        default=1,
        validators=[MinValueValidator(1, "Can't make a booking with 0 or less persons")],
    )
    status = models.TextField(
        max_length=10,
        choices=BookingStatusEnum.choices,
        default=BookingStatusEnum.WAITING,
        blank=True,
    )
    start_date = models.DateTimeField(validators=[MinValueValidator(timezone.now)])
    end_date = models.DateTimeField(validators=[MinValueValidator(timezone.now)])

    class Meta:
        ordering = ["thing", "start_date"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F("start_date")), name="end_date__gt__start_date"
            )
        ]

    def __str__(self) -> str:
        return f"From {self.start_date} to {self.end_date} for {str(self.thing)}"


class Rule(ThingbookerModel):
    """
    Model for a rule.

    A rule can be extra context about the thing it is related to, such as how
    you should leave the thing after done, or general information.
    """

    short = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)

    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name="rules")

    class Meta:
        order_with_respect_to = "thing"

    def __str__(self) -> str:
        return f"Rule {self.short} for {self.thing}"
