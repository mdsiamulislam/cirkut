from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserPresence

User = get_user_model()

@receiver(post_save, sender=User)
def create_presence(sender, instance, created, **kwargs):
    if created:
        UserPresence.objects.create(user=instance)