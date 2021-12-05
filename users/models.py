from django.conf import settings

import pytz
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


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


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDERS = (
        (MALE, "Man"),
        (FEMALE, "Woman")
    )

    user = models.OneToOneField(User, null=False, unique=True, on_delete=models.CASCADE, db_index=True)
    tagline = models.CharField(max_length=128, verbose_name='Tags', blank=True)
    about_me = models.TextField(verbose_name='About Me')
    gender = models.CharField(choices=GENDERS, default=MALE, verbose_name='Sex', max_length=1)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
