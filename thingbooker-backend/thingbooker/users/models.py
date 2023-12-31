"""Contains models for the authentication app."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_image_file_extension
from django.db import models

from thingbooker.base_models import ThingbookerModel

if TYPE_CHECKING:
    from django.db.models.manager import ManyToManyRelatedManager


def user_avatar_path(instance: ThingbookerUser, filename: str):
    """Get's the avatar upload path for a given user."""

    extension = filename.split(".")[-1]
    return f"users/avatars/{instance.id}.{extension}"


def group_picture_path(instance: ThingbookerGroup, filename: str):
    """Fetches the group picture upload path for a given group."""

    extension = filename.split(".")[-1]
    return f"groups/pictures/{instance.id}.{extension}"


class ThingbookerUser(AbstractUser, ThingbookerModel):
    """User of thingbooker."""

    username = models.EmailField(
        blank=False, verbose_name="email address", unique=True, db_index=True
    )
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        null=True,
        validators=[validate_image_file_extension],
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

    # specify name since we can have multiple with the same name
    name = models.CharField(max_length=150)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="thingbooker_group")
    group_picture = models.ImageField(upload_to=group_picture_path, null=True)

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    @property
    def members(self) -> ManyToManyRelatedManager[ThingbookerUser]:
        """Shorthand for accessing the userset of auth.Group model."""

        return self.group.user_set
