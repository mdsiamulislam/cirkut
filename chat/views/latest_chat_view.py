from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


from chat.models import Connection, ChatMessage
from account.models import UserPresence

from chat.serializers.chat_serializer import ChatMessageSerializer


class LatestChatView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        connections = Connection.objects.filter(user=user) | Connection.objects.filter(friend=user)

        print(f"User: {user.username}, Connections: {connections.count()}")

        latest_chats = []
        for connection in connections:
            room_name = connection.room_name
            latest_message = ChatMessage.objects.filter(room_name=room_name).order_by('-timestamp').first()
            if latest_message:
                serializer = ChatMessageSerializer(latest_message)
                latest_chats.append(serializer.data)
        return Response(latest_chats, status=status.HTTP_200_OK)