from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from account.models import UserPresence
from account.serializers.user_presence_serializer import UserPresenceSerializer

class UserPresenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # All user presence data
        presences = UserPresence.objects.all()
        serializer = UserPresenceSerializer(presences, many=True)
        return Response(serializer.data)


class SelectedUserPresenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Get specific user presence data
        try:
            presence = UserPresence.objects.get(user_id=user_id)
        except UserPresence.DoesNotExist:
            return Response({"detail": "User presence not found"}, status=404)
        serializer = UserPresenceSerializer(presence)
        return Response(serializer.data)