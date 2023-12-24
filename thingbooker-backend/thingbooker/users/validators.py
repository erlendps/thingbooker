from django.core.exceptions import ValidationError
from PIL.Image import Image


def validate_image_is_square(value: Image):
    """Validates that the image is square (aspect ration 1:1)."""

    if value.height != value.width:
        raise ValidationError(
            "Image dimensions has to be of same size. Got %(w)sx%(h)s.",
            params={"w": value.width, "h": value.height},
        )
