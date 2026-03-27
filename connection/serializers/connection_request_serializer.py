from rest_framework import serializers
from connection.models.user_connection_model import ConnectionRequest
from account.serializers.user_data_serializer import UserPublicDataSerializer

class ConnectionRequestSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()  # new field for the "other user"

    class Meta:
        model = ConnectionRequest
        fields = ['id', 'friend', 'status', 'created_at']  # keep response similar
        read_only_fields = ['id', 'created_at']

    def get_friend(self, obj):
        user = self.context['request'].user  # current logged-in user
        other_user = obj.receiver if obj.sender == user else obj.sender
        return UserPublicDataSerializer(other_user).data