from django.contrib import admin
from django.contrib.auth import get_user_model
from guardian.admin import GuardedModelAdmin

from thingbooker.users.models import ThingbookerGroup


@admin.register(ThingbookerGroup)
class GuardedAdmin(GuardedModelAdmin):
    """User admin with objects permission support"""

    pass


admin.site.register(get_user_model(), GuardedAdmin)
