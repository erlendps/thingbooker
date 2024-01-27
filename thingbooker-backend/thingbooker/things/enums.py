from django.db.models import TextChoices


class BookingStatusEnum(TextChoices):
    """Enum for booking status"""

    DECLINED = ("declined", "Booking is declined")
    ACCEPTED = ("accepted", "Booking is accepted")
    WAITING = ("waiting", "Booking is waiting for approval")

    @classmethod
    def update_choices(cls):
        """Returns choices for when updating a booking"""

        return [choice for choice in cls.choices if choice[0] != cls.WAITING]
