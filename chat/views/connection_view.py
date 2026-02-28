from rest_framework.views import APIView, connections
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from chat.serializers.connection_serializer import ConnectionSerializer
from chat.models import Connection


class ConnectionListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        connections = Connection.objects.filter(user=user) | Connection.objects.filter(friend=user)
        serializer = ConnectionSerializer(connections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)