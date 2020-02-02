import os

from django.conf import settings
from django.utils.timezone import localtime, now

from crdb.models import *


user = Person.objects.first()
