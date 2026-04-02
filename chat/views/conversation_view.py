from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from chat.models import Conversation
from chat.serializers.conversation_serializar import ConversationSerializer


class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        conversations = Conversation.objects.filter(participants=user).order_by('-updated_at')
        serializer = ConversationSerializer(conversations, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        participant_ids = request.data.get('participant_ids', [])
        if not participant_ids:
            return Response({'detail': 'Participant IDs are required.'}, status=status.HTTP_400_BAD_REQUEST)

        lenth = len(participant_ids)
        print(lenth)
        if lenth < 2:
            participants = Conversation.objects.filter(participants__id__in=participant_ids).distinct()
            if participants.exists():
                conversation = participants.first()
                serializer = ConversationSerializer(conversation, context={'request': request})
                return Response({
                    'detail': 'Conversation already exists.',
                    'conversation': serializer.data
                }, status=status.HTTP_200_OK)

        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids + [user.id])
        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
