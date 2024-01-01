from dj_rest_auth.registration.views import VerifyEmailView
from django.contrib import admin
from django.urls import include, path

from thingbooker.router import router

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "auth/account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    path("admin/", admin.site.urls),
]
