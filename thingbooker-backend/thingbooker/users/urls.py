from rest_framework.routers import SimpleRouter

from thingbooker.users.views import GroupInviteTokenViewSet, GroupViewSet, UserViewSet

router = SimpleRouter()

router.register("accounts", UserViewSet, basename="thingbookeruser")
router.register("groups", GroupViewSet, basename="thingbookergroup")
router.register(
    "group-invite-tokens", GroupInviteTokenViewSet, basename="thingbooker-group-invite-token"
)
