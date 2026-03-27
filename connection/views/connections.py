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
    

class ConnectionActionView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, connection_id):
        user = request.user
        try:
            connection_request = ConnectionRequest.objects.get(id=connection_id, receiver=user, status='accepted')
            connection_request.delete()
            return Response({'detail': 'Connection request deleted.'}, status=status.HTTP_200_OK)
        except ConnectionRequest.DoesNotExist:
            return Response({'detail': 'Connection request not found.'}, status=status.HTTP_404_NOT_FOUND)