"""Contains models for the authentication app."""
from __future__ import annotations

from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_image_file_extension
from django.db import models

from thingbooker.base_models import ThingbookerModel
from thingbooker.users.validators import validate_image_is_square


def user_avatar_path(instance: ThingbookerUser, filename: str):
    """Get's the avatar upload path for a given user."""

    extension = filename.split(".")[-1]
    return f"users/avatars/{instance.id}.{extension}"


class ThingbookerUser(AbstractUser, ThingbookerModel):
    """User of thingbooker."""

    username = models.EmailField(
        blank=False, verbose_name="email address", unique=True, db_index=True
    )
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        null=True,
        validators=[validate_image_file_extension, validate_image_is_square],
    )

    def save(self, *args, **kwargs):
        """Set the email field the same as the username (email is username)."""

        if not self.email:
            self.email = self.username
        return super().save(*args, **kwargs)

    def get_group_or_none(self, group_id: int) -> Group | None:
        """Fetches the group (only looks at this users group)."""

        try:
            return self.groups.get(pk=group_id)
        except ObjectDoesNotExist:
            return None

    def get_all_groups(self):
        """Fetches all groups for this user."""

        return self.groups.select_related("thingbooker_group").all()


class ThingbookerGroup(models.Model):
    """
    A group is a collection of users.

    In thingbooker, it is used as a convenience to quickly share a new thing.
    It also has some extra fields. For now it's nothing extra, but in the future,
    this allows for easy extension of a group.
    """

    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="thingbooker_group")
