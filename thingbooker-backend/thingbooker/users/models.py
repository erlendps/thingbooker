"""Contains models for the authentication app."""
from __future__ import annotations

from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from thingbooker.base_models import ThingbookerModel


class ThingbookerUser(AbstractUser, ThingbookerModel):
    """User of thingbooker."""

    email = models.EmailField(
        blank=False, max_length=254, verbose_name="email address", unique=True
    )

    def get_group_or_none(self, group_id: int) -> Group | None:
        """Fetches the group (only looks at this users group)."""

        try:
            return self.groups.get(pk=group_id)
        except ObjectDoesNotExist:
            return None
