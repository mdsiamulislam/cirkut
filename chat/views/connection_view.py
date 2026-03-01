from rest_framework.views import APIView, connections
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from account.models import User
from chat.serializers.connection_serializer import ConnectionSerializer
from chat.models import Connection
from chat.serializers.utils.massage_notification import send_notification


class ConnectionListView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        connections = Connection.objects.filter(user=user) | Connection.objects.filter(friend=user)
        serializer = ConnectionSerializer(connections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        friend_user_name = request.data.get('friend_username')
        if not friend_user_name:
            return Response({"error": "Friend username is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            friend_user = User.objects.get(username=friend_user_name)
        except User.DoesNotExist:
            return Response({"error": "Friend user not found"}, status=status.HTTP_404_NOT_FOUND)
        user = request.user
        if Connection.objects.filter(user=user, friend=friend_user).exists() or Connection.objects.filter(user=friend_user, friend=user).exists():
            return Response({"error": "Connection already exists"}, status=status.HTTP_400_BAD_REQUEST)
        connection = Connection.objects.create(user=user, friend=friend_user)
        serializer = ConnectionSerializer(connection)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class NotificationTestView(APIView):
    def get(self, request):
        token = 'eJ89IigRShS-soaj6V0IJF:APA91bFfsKW0mqx3oSg410L7wNWJrTgGwHUfJ_IsCTv3YfDjtbJIYTkNVD3RQD_17ah6L5lYO_K7UV__IBQTI575kTQFdBEmH3ECxbN7cQwltiVgVuIhpf4'
        title = 'Test Notification'
        body = 'This is a test notification from Firebase.'
        
        # ফাংশন কল করা হচ্ছে
        response = send_notification(token, title, body)
        
        # সাকসেস রেসপন্স ব্যাক করা হচ্ছে
        return Response({
            "message": "Notification process completed",
            "firebase_response": response
        })