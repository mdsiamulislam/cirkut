from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from connection.models.user_connection_model import ConnectionRequest
from connection.serializers.connection_request_serializer import ConnectionRequestSerializer


class ConnectionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        received_requests = ConnectionRequest.objects.filter(receiver=user, status='accepted')
        received_serializer = ConnectionRequestSerializer(received_requests, many=True)
        
        return Response(received_serializer.data, status=status.HTTP_200_OK)