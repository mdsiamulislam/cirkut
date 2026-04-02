from django.db import models
from django.conf import settings

class Connection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='connections')
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='connected_with')
    room_name = models.CharField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Genarate automatically unique room name
    def save(self, *args, **kwargs):
        if not self.room_name:
            sorted_users = sorted([self.user.id, self.friend.id])
            self.room_name = f"room_{sorted_users[0]}_{sorted_users[1]}"
        super().save(*args, **kwargs)
    class Meta:
        unique_together = ('user', 'friend')


class Conversation(models.Model):
    # Duijon user-er moddhe connection
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # Shesh message-er shomoy track rakhar jonno

    def __str__(self):
        return f"Conversation {self.id}"
    
class ChatMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] # Purono message agey, notun niche

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"

class GroupChat(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_chats')
    room_name = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    room_name = models.CharField(max_length=100)
    message = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.room_name}] {self.user}: {self.message}"

class MessageNotificationToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.token}"
