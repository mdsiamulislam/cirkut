from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from chat.models import ChatMessage, Connection
from chat.serializers.chat_serializer import ChatMessageSerializer

class ChatListView(APIView):
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
                # Get Friend's data
                friend = connection.friend if connection.user == user else connection.user
                latest_message.user = friend
                serializer = ChatMessageSerializer(latest_message)
                latest_chats.append(serializer.data)
                latest_chats.sort(key=lambda x: x['timestamp'], reverse=True)
        return Response(latest_chats)