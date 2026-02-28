from django.db import models
from django.contrib.auth.models import AbstractUser
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