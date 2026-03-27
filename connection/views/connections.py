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
        connections = ConnectionRequest.objects.filter(receiver=user, status='accepted') | ConnectionRequest.objects.filter(sender=user, status='accepted')
        serializer = ConnectionRequestSerializer(connections, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class ConnectionActionView(APIView):
    permission_classes = [IsAuthenticated]

    # Send Connection Request
    def post(self, request, connection_id):
        user = request.user

        # Check if the connection request already exists
        if ConnectionRequest.objects.filter(sender=user, receiver_id=connection_id, status='pending').exists():
            return Response({'detail': 'Connection request already sent. Awaiting acceptance.'}, status=status.HTTP_400_BAD_REQUEST)
        if ConnectionRequest.objects.filter(sender_id=connection_id, receiver=user, status='pending').exists():
            return Response({'detail': 'You have already received a connection request from this user. Awaiting acceptance.'}, status=status.HTTP_400_BAD_REQUEST)
        if ConnectionRequest.objects.filter(sender=user, receiver_id=connection_id, status='accepted').exists():
            return Response({'detail': 'You are already connected with this user.'}, status=status.HTTP_400_BAD_REQUEST)
        if ConnectionRequest.objects.filter(sender_id=connection_id, receiver=user, status='accepted').exists():
            return Response({'detail': 'You are already connected with this user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Also if get request exists, then we can directly accept the connection request instead of creating a new one
        existing_request = ConnectionRequest.objects.filter(sender_id=connection_id, receiver=user, status='pending').first()
        if existing_request:
            existing_request.status = 'accepted'
            existing_request.save()
            return Response({'detail': 'Connection request accepted.'}, status=status.HTTP_200_OK)
        
        
        # Create a new connection request
        connection_request = ConnectionRequest.objects.create(sender=user, receiver_id=connection_id)
        serializer = ConnectionRequestSerializer(connection_request,context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def delete(self, request, connection_id):
        user = request.user
        try:
            connection_request = ConnectionRequest.objects.get(id=connection_id, receiver=user, status='accepted')
            connection_request.delete()
            return Response({'detail': 'Connection request deleted.'}, status=status.HTTP_200_OK)
        except ConnectionRequest.DoesNotExist:
            return Response({'detail': 'Connection request not found.'}, status=status.HTTP_404_NOT_FOUND)