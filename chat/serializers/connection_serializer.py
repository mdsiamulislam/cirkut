from rest_framework import serializers
from chat.models import Connection
from django.contrib.auth import get_user_model
from account.serializers.user_data_serializer import UserPublicDataSerializer

User = get_user_model()

class ConnectionSerializer(serializers.ModelSerializer):
    friend = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    user = UserPublicDataSerializer(read_only=True)
    friend_data = UserPublicDataSerializer(source='friend', read_only=True)

    class Meta:
        model = Connection
        fields = ['id', 'user', 'friend', 'friend_data', 'room_name', 'created_at']
        read_only_fields = ['room_name']