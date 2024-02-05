import os

from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models.signals import post_delete
from django.dispatch import receiver

from thingbooker.things.models import Thing
from thingbooker.users.models import ThingbookerGroup, ThingbookerUser


@receiver(post_delete, sender=Thing)
@receiver(post_delete, sender=ThingbookerGroup)
@receiver(post_delete, sender=ThingbookerUser)
def auto_delete_related_image(_, instance, **kwargs):
    """Deletes images when the object is deleted"""

    if not isinstance(default_storage, FileSystemStorage):
        # don't handle
        return

    if isinstance(instance, Thing):
        if instance.picture and os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)
    elif isinstance(instance, ThingbookerGroup):
        if instance.group_picture and os.path.isfile(instance.group_picture.path):
            os.remove(instance.group_picture.path)
    elif isinstance(instance, ThingbookerUser):
        if instance.avatar and os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)
