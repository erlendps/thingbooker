from rest_framework.routers import SimpleRouter

from thingbooker.things.views import BookingViewSet, RuleViewSet, ThingViewSet

router = SimpleRouter()

router.register("bookings", BookingViewSet, basename="booking")
router.register("rules", RuleViewSet, basename="rule")
router.register("things", ThingViewSet, basename="thing")
