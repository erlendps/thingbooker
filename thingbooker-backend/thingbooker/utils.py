import hashlib
from base64 import urlsafe_b64encode
from os import urandom

from django.conf import settings


def create_token(length: int = settings.TOKEN_BYTE_LENGTH):
    """Creates a token using urandom."""

    random = urandom(length)
    token = urlsafe_b64encode(random)[:-1]  # remove = suffix of base64
    return token.decode("utf-8")


def hash_token(token: str):
    """Hashes the given string using sha256"""

    sha256 = hashlib.sha256()
    sha256.update(bytes(token, "utf-8"))
    return sha256.hexdigest()
