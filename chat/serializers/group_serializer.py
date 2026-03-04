from rest_framework import serializers
from django.utils import timezone
from chat.models import GroupChat
from django.conf import settings


class GroupChatSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset= settings.AUTH_USER_MODEL.objects.all()
    )

    class Meta:
        model = GroupChat
        fields = ['id', 'name', 'members', 'room_name', 'created_at']
        read_only_fields = ['room_name', 'created_at']

    def create(self, validated_data):
        members = validated_data.pop('members')

        group_name = validated_data['name']
        timestamp = int(timezone.now().timestamp())
        room_name = f"group_{group_name}_{timestamp}"

        group = GroupChat.objects.create(
            room_name=room_name,
            **validated_data
        )

        group.members.set(members)
        return group