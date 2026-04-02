from rest_framework import serializers
from chat.models import Conversation

from account.serializers.user_data_serializer import UserPublicDataSerializer

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserPublicDataSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'updated_at']


    # Remove Current User from Participants List
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     request = self.context.get('request')
    #     if request and hasattr(request, 'user'):
    #         current_user = request.user
    #         representation['participants'] = [participant for participant in representation['participants'] if participant['id'] != current_user.id]
    #     return representation