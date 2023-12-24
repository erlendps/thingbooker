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

SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS: list[str] = ["*"]

CLIENT_URL = config("FRONTEND_URL")

ROOT_URLCONF = "thingbooker.urls"

WSGI_APPLICATION = "thingbooker.wsgi.application"

LOCAL_APPS = [
    "thingbooker.users",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "guardian",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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


########################
# Internationalization #
########################

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True

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
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    )
}

###################
# REST simple JWT #
###################

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer", "JWT"),
}
