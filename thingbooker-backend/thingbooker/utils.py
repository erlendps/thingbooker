from base64 import urlsafe_b64encode
from os import urandom

from django.conf import settings


def create_token(length: int = settings.TOKEN_BYTE_LENGTH):
    """Creates a token using urandom."""

    random = urandom(length)
    token = urlsafe_b64encode(random)[:-1]  # remove = suffix of base64
    return token.decode("utf-8")
