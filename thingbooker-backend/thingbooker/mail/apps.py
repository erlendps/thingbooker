from django.apps import AppConfig


class MailConfig(AppConfig):
    """Mail config"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "thingbooker.mail"
