"""Contains models for the authentication app."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_image_file_extension
from django.db import models
from django.utils import timezone

from thingbooker.base_models import ThingbookerManager, ThingbookerModel
from thingbooker.utils import create_token

if TYPE_CHECKING:
    from django.db.models.manager import ManyToManyRelatedManager, RelatedManager

    from thingbooker.things.models import Booking, Thing


def user_avatar_path(instance: ThingbookerUser, filename: str):
    """Get's the avatar upload path for a given user."""

    extension = filename.split(".")[-1]
    return f"users/avatars/{instance.id}.{extension}"


def group_picture_path(instance: ThingbookerGroup, filename: str):
    """Fetches the group picture upload path for a given group."""

    extension = filename.split(".")[-1]
    return f"groups/pictures/{instance.id}.{extension}"


class ThingbookerUserManager(UserManager):
    """Custom manager for thingbooker users."""

    def get_or_none(self, *args, **kwargs):
        """Tries fetching the user, if it does not exist, return None"""

        try:
            return self.get(*args, **kwargs)
        except ObjectDoesNotExist:
            return None


class ThingbookerUser(AbstractUser, ThingbookerModel):
    """User of thingbooker."""

    if TYPE_CHECKING:
        bookings: RelatedManager[Booking]
        owned_things: RelatedManager[Thing]
        things: RelatedManager[Thing]

    username = models.EmailField(
        blank=False, verbose_name="email address", unique=True, db_index=True
    )
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        null=True,
        validators=[validate_image_file_extension],
    )

    objects: ThingbookerUserManager = ThingbookerUserManager()

    @property
    def thingbooker_groups(self):
        """Returns a queryset of related ThingbookerGroup instances"""

        return ThingbookerGroup.objects.filter(group__user=self)

    @property
    def is_admin_user(self):
        """Returns true if this user is an admin user"""

        return self.is_staff or self.is_superuser

    def save(self, *args, **kwargs):
        """Set the email field the same as the username (email is username)."""

        if not self.email:
            self.email = self.username
        return super().save(*args, **kwargs)

    def get_all_known_users(self):
        """Fetches the users that this user 'knows', i.e is in a group with."""

        return get_user_model().objects.filter(groups__in=self.groups.all())

    def get_group_or_none(self, group_id: int) -> Group | None:
        """Fetches the group (only looks at this users group)."""

        try:
            return self.groups.get(pk=group_id).thingbooker_group
        except ObjectDoesNotExist:
            return None

    def get_all_groups(self):
        """Fetches all thingbooker groups for this user."""

        return self.groups.select_related("thingbooker_group").all()


class ThingbookerGroup(ThingbookerModel):
    """
    A group is a collection of users.

    In thingbooker, it is used as a convenience to quickly share a new thing.
    It also has some extra fields. For now it's nothing extra, but in the future,
    this allows for easy extension of a group.
    """

    # specify name since we can have multiple with the same name
    name = models.CharField(max_length=150)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="thingbooker_group")
    group_picture = models.ImageField(upload_to=group_picture_path, null=True, blank=True)

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    @property
    def members(self) -> ManyToManyRelatedManager[ThingbookerUser]:
        """Shorthand for accessing the userset of auth.Group model."""

        return self.group.user_set

    def user_is_member(self, user: ThingbookerUser):
        """Returns True if the user is a member of this group."""

        return self.members.contains(user)


class GenericToken(ThingbookerModel):
    """Generic abstract token class."""

    token = models.CharField(max_length=256, editable=False, db_index=True)

    expires_at = models.DateTimeField(editable=False)

    used_at = models.DateTimeField(null=True, blank=True)

    objects: ThingbookerManager = ThingbookerManager()

    @property
    def is_expired(self):
        """Checks if the token has expired."""

        return timezone.now() > self.expires_at

    @property
    def is_used(self):
        """Checks if the token has been used."""

        return bool(self.used_at)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-expires_at"]

    def __str__(self) -> str:
        return f"Token: {self.token}, Created: {self.created_at}, Expires: {self.expires_at}"

    def save(self, *args, **kwargs):
        """Generate the token on save."""

        if not self.created_at:
            self.created_at = timezone.now()
        if not self.expires_at:
            self.expires_at = self.created_at + timezone.timedelta(days=settings.TOKEN_EXPIRY)
        if not self.token:
            self.token = create_token()
        super().save(*args, **kwargs)

    def get_clickable_url(self, token_action: str) -> str:
        """Returns a 'clickable' url that is sent in the mail to the user being invited."""

        return f"{settings.CLIENT_BASE_URL}invite-tokens/{token_action}/{self.token}/"

    def is_invalid(self):
        """Checks if the token is valid"""

        return self.is_used or self.is_expired


class AcceptInviteToken(GenericToken):
    """
    Token for accepting an invite.

    Has user, which is the invited user and
    group, which is the group the email is invited to.
    """

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="group_invites",
    )

    group = models.ForeignKey(
        ThingbookerGroup,
        on_delete=models.CASCADE,
        related_name="invite_tokens",
    )

    class Meta:
        unique_together = ("user", "token")

    def get_clickable_url(self) -> str:
        """Returns a 'clickable' url that is sent in the mail to the user being invited."""

        return super().get_clickable_url("accept-invite")

    def __str__(self) -> str:
        return "AcceptInvite" + super().__str__()
