from rest_framework import serializers

from chat.models import MessageNotificationToken

class MessageNotificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageNotificationToken
        fields = ['user', 'token']