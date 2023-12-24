from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from thingbooker.users.views import UserViewSet

router = DefaultRouter()
router.register("account", UserViewSet, basename="thingbookeruser")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("account/", include("thingbooker.users.urls")),
]
