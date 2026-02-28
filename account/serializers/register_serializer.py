from rest_framework import serializers
from account.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'profile_picture')
        extra_kwargs = {
            'username': {'required': False}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username= User.generate_username(User),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            profile_picture=validated_data.get('profile_picture', '')
        )
        return user
    


class GoogleRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'google_id', 'profile_picture')
        extra_kwargs = {
            'username': {'required': False},
            'password': {'required': False}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username= User.generate_username(User),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            google_id=validated_data['google_id'],
            profile_picture=validated_data.get('profile_picture', '')
        )
        return user