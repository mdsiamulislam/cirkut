from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from chat.serializers.noification_serializer import MessageNotificationTokenSerializer
from chat.models import MessageNotificationToken



class NotificationRegisterView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        token = request.data.get('token')

        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Database e save
        notification_token, created = MessageNotificationToken.objects.update_or_create(
            user=user,
            defaults={'token': token}
        )

        serializer = MessageNotificationTokenSerializer(notification_token)
        return Response(serializer.data, status=status.HTTP_201_CREATED)