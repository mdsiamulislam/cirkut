from rest_framework import serializers

from chat.models import Connection
from account.serializers.user_data_serializer import UserPublicDataSerializer

class ConnectionSerializer(serializers.ModelSerializer):
    friend = UserPublicDataSerializer(read_only=True)
    user = UserPublicDataSerializer(read_only=True)
    class Meta:
        model = Connection
        fields = ['id', 'user', 'friend', 'created_at']