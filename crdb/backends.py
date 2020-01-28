from django.conf import settings

from crdb.models import Person


class EmailOrUsernameModelBackend(object):

    def authenticate(self, request, username=None, password=None):
        try:
            username = username.lower()
            if '@' in username:
                person = Person.objects.by_email(username)
            else:
                person = Person.objects.get(username=username)
            if person.check_password(password):
                return person
        except Exception:
            return None

    def get_user(self, id):
        try:
            return Person.objects.get(pk=id)
        except Person.DoesNotExist:
            return None
