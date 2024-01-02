from rest_framework.routers import DefaultRouter

from thingbooker.users.views import GroupViewSet, InviteTokenViewSet, UserViewSet

router = DefaultRouter()

router.register("accounts", UserViewSet, basename="thingbookeruser")
router.register("groups", GroupViewSet, basename="thingbookergroup")
router.register("invite-tokens", InviteTokenViewSet, basename="thingbooker-invite-token")
