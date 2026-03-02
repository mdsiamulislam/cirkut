from rest_framework import serializers
from account.models import UserPresence

class UserPresenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPresence
        fields = ['user', 'is_online', 'last_seen']