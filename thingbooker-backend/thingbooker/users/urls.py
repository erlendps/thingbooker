from rest_framework.routers import SimpleRouter

from thingbooker.users.views import GroupViewSet, InviteTokenViewSet, UserViewSet

router = SimpleRouter()

router.register("accounts", UserViewSet, basename="thingbookeruser")
router.register("groups", GroupViewSet, basename="thingbookergroup")
router.register("invite-tokens", InviteTokenViewSet, basename="thingbooker-invite-token")
