from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import include, path

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path(
        "account-confirm-email/", VerifyEmailView.as_view(), name="account_email_verification_sent"
    ),
]
