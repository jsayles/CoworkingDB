from django.conf import settings
from django.utils.timezone import localtime, now
from django.core.exceptions import ImproperlyConfigured

from pydiscourse import DiscourseClient


class DiscourseAPI:

    def __init__(self) -> None:
        self.discourse_url = getattr(settings, 'DISCOURSE_URL', None)
        if not self.discourse_url:
            raise ImproperlyConfigured("Missing DISCOURSE_URL setting.")

        self.discourse_user = getattr(settings, 'DISCOURSE_USER', None)
        if not self.discourse_user:
            raise ImproperlyConfigured("Missing DISCOURSE_USER setting.")

        self.discourse_key = getattr(settings, 'DISCOURSE_KEY', None)
        if not self.discourse_key:
            raise ImproperlyConfigured("Missing DISCOURSE_KEY setting.")

        self.client = DiscourseClient(
            self.discourse_url,
            api_username = self.discourse_user,
            api_key = self.discourse_key
        )
