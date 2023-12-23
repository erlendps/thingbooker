"""This contains base models used in the app."""

from uuid import uuid4

from django.db import models
from django.utils import timezone


class UUIDBase(models.Model):
    """Use UUID as a models primary key."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class CreatedAtBase(models.Model):
    """Keep track of when a model was created."""

    created_at = models.DateTimeField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Set created at if not already set"""

        if self.created_at is None:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)


class UpdatedAtBase(models.Model):
    """Keep track of when a model instance was updated."""

    updated_at = models.DateTimeField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Update updated_at on each save."""

        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)


class TimestampBase(CreatedAtBase, UpdatedAtBase):
    """Track when object has been created and last updated."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        We want to have the same date for created at and updated at when the object
        is first created.
        """

        now = timezone.now()
        if self.created_at is None:
            self.created_at = now
        self.updated_at = now
        return super().save(*args, **kwargs)


class ThingbookerModel(UUIDBase, TimestampBase):
    """Base model for Thingbooker"""

    class Meta:
        abstract = True
        get_latest_by = "created_at"
        ordering: tuple[str, ...] = ("-created_at",)
