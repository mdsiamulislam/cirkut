from rest_framework import serializers
from account.models import User

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'profile_picture', 
            'google_id'
        )
        # exclude = ('password', 'google_id')

class UserPublicDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name', 
            'last_name', 
            'profile_picture'
        )