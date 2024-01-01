from rest_framework.routers import DefaultRouter

from thingbooker.users.views import GroupViewSet, UserViewSet

router = DefaultRouter()

router.register("account", UserViewSet, basename="thingbookeruser")
router.register("groups", GroupViewSet, basename="thingbookergroup")
