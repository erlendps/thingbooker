from dj_rest_auth.registration.views import VerifyEmailView
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from thingbooker.things.urls import router as things_router
from thingbooker.users.urls import router as users_router

# extend top-router with app specific routers
router = DefaultRouter()
router.registry.extend(users_router.registry)
router.registry.extend(things_router.registry)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "auth/account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    path("django-admin/", admin.site.urls),
]
