from django.conf import settings

import pytz
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True)

    activate_key = models.CharField(max_length=128, verbose_name='Activation key', blank=True, null=True)
    activate_key_expired = models.DateTimeField(blank=True, null=True)

    def is_activate_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.activate_key_expired + timedelta(hours=48):
            return True
        return False

    def activate(self):
        self.is_active = True
        self.activate_key = None
        self.activate_key_expired = None
        self.save()
