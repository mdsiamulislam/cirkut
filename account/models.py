from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.URLField(blank=True, null=True)
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __str__(self):
        return self.first_name
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_username()

        # If google id then set password to unusable
        if self.google_id:
            self.set_unusable_password()
        super().save(*args, **kwargs)

    def generate_username(self):
        return uuid.uuid4().hex
    

class UserPresence(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)

    def set_online(self):
        self.is_online = True
        self.save(update_fields=['is_online'])

    def set_offline(self):
        self.is_online = False
        self.last_seen = timezone.now()
        self.save(update_fields=['is_online', 'last_seen'])

    def __str__(self):
        return f"{self.user} - {'Online' if self.is_online else 'Offline'}"
    