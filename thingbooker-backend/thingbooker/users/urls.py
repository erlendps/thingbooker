from rest_framework.routers import SimpleRouter

from thingbooker.users.views import (
    GroupInviteTokenViewSet,
    GroupViewSet,
    ThingInviteTokenViewSet,
    UserViewSet,
)

router = SimpleRouter()

router.register("accounts", UserViewSet, basename="thingbookeruser")
router.register("groups", GroupViewSet, basename="thingbookergroup")
router.register("group-invite-tokens", GroupInviteTokenViewSet, basename="acceptgroupinvitetoken")
router.register("thing-invite-tokens", ThingInviteTokenViewSet, basename="acceptthinginvitetoken")
