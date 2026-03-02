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