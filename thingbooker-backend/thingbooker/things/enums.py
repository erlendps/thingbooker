from django.db.models import TextChoices


class BookingStatusEnum(TextChoices):
    """Enum for booking status"""

    DECLINED = ("declined", "Booking is declined")
    ACCEPTED = ("accepted", "Booking is accepted")
    WAITING = ("waiting", "Booking is waiting for approval")
