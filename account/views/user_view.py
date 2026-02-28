from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from account.serializers.user_data_serializer import UserDataSerializer
from account.models import User

class UserDataView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDataSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)