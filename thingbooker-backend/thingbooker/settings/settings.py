"""This module contains the settings for thingbooker-backend"""

import os
from datetime import timedelta

from decouple import config

#####################
#####################
## Django settings ##
#####################
#####################

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# security
SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS: list[str] = config("ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")])

SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)

SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=True, cast=bool)

CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=True, cast=bool)

CLIENT_URL = config("FRONTEND_URL")

ROOT_URLCONF = "thingbooker.urls"

WSGI_APPLICATION = "thingbooker.wsgi.application"

LOCAL_APPS = [
    "thingbooker.users",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "guardian",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


#############
# Databases #
#############

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

##################
# AUTHENTICATION #
##################

AUTH_USER_MODEL = "users.ThingbookerUser"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # default
    "guardian.backends.ObjectPermissionBackend",
)

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URL = "/home/"


########################
# Internationalization #
########################

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True

#########
# email #
#########

DEFAULT_FROM_EMAIL = "account@thingbooker.no"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
EMAIL_TIMEOUT = config("EMAIL_TIMEOUT", default=None, cast=lambda x: int(x) if x else None)
EMAIL_BACKEND = config("EMAIL_BACKEND")

####################
# Static and media #
####################

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "thingbooker", "static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "thingbooker", "common-static")]

MEDIA_URL = "uploads/"
MEDIA_ROOT = os.path.join(BASE_DIR, "thingbooker", "uploads")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

###################################
###################################
## Third-party app configuration ##
###################################
###################################

##################
# REST framework #
##################

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    )
}

###################
# REST simple JWT #
###################

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=config("ACCESS_TOKEN_LIFETIME", cast=int)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=config("REFRESH_TOKEN_LIFETIME", cast=int)),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer", "JWT"),
}

################
# dj rest auth #
################

REST_AUTH = {
    # serializers
    "USER_DETAILS_SERIALIZER": "dj_rest_auth.serializers.UserDetailsSerializer",
    "REGISTER_SERIALIZER": "dj_rest_auth.registration.serializers.RegisterSerializer",
    # auth
    "PASSWORD_RESET_USE_SITES_DOMAIN": False,
    "OLD_PASSWORD_FIELD_ENABLED": True,
    # jwt
    "USE_JWT": True,
    "SESSION_LOGIN": False,
    "JWT_AUTH_COOKIE": "thingbooker-access-token",
    "JWT_AUTH_REFRESH_COOKIE": "thingbooker-refresh-token",
    "JWT_AUTH_SECURE": config("JWT_AUTH_SECURE", default=True, cast=bool),
    "JWT_AUTH_HTTPONLY": config("JWT_AUTH_HTTPONLY", default=True, cast=bool),
    "JWT_AUTH_COOKIE_USE_CSRF": config("JWT_AUTH_COOKIE_USE_CSRF", default=True, cast=bool),
    "JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED": config(
        "JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED", default=True, cast=bool
    ),
}

##################
# django allauth #
##################

ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Thingbooker] "
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = config("ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS", default=False, cast=bool)
ACCOUNT_DEFAULT_HTTP_PROTOCOL = config("ACCOUNT_DEFAULT_HTTP_PROTOCOL", default="https")
ACCOUNT_PRESERVE_USERNAME_CASING = False
