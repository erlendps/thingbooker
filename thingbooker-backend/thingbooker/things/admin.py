from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from thingbooker.things.models import Booking, Rule, Thing


@admin.register(Thing)
class ThingAdmin(GuardedModelAdmin):
    """Admin for thing"""

    pass


admin.site.register([Booking, Rule])
