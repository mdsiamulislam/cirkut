from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from connection.models.user_connection_model import ConnectionRequest
from connection.serializers.connection_request_serializer import ConnectionRequestSerializer


class ConnectionRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        received_requests = ConnectionRequest.objects.filter(receiver=user, status='pending')
        received_serializer = ConnectionRequestSerializer(received_requests, many=True, context={'request': request})

        return Response(received_serializer.data, status=status.HTTP_200_OK)
    
class ConnectionRequestActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        user = request.user
        try:
            connection_request = ConnectionRequest.objects.get(id=request_id, receiver=user, status='pending')
            connection_request.status = 'accepted'
            connection_request.created_at = timezone.now()
            connection_request.save()
            return Response({'detail': 'Connection request accepted.'}, status=status.HTTP_200_OK)
        except ConnectionRequest.DoesNotExist:
            return Response({'detail': 'Connection request not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, request_id):
        user = request.user
        try:
            connection_request = ConnectionRequest.objects.get(id=request_id, receiver=user, status='pending')
            connection_request.status = 'rejected'
            connection_request.save()
            return Response({'detail': 'Connection request rejected.'}, status=status.HTTP_200_OK)
        except ConnectionRequest.DoesNotExist:
            return Response({'detail': 'Connection request not found.'}, status=status.HTTP_404_NOT_FOUND)