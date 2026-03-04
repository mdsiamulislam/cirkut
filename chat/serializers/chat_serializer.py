from rest_framework import serializers
from chat.models import ChatMessage
from account.serializers.user_data_serializer import UserPublicDataSerializer
class ChatMessageSerializer(serializers.ModelSerializer):
    user = UserPublicDataSerializer(read_only=True)
    class Meta:
        model = ChatMessage
        fields = '__all__'