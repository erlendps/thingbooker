from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from thingbooker.users.views import UserViewSet

router = DefaultRouter()
router.register("", UserViewSet, basename="user")

urlpatterns = [
    # readonly user
    path("", include(router.urls)),
    # jwt token management
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
