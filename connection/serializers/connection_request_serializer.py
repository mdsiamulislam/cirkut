from rest_framework import serializers
from connection.models.user_connection_model import ConnectionRequest
from account.serializers.user_data_serializer import UserPublicDataSerializer

class ConnectionRequestSerializer(serializers.ModelSerializer):
    sender = UserPublicDataSerializer(read_only=True)
    class Meta:
        model = ConnectionRequest
        fields = ['id', 'sender', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']
