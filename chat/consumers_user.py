import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from account.models import UserPresence

class UserConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']

        if not user.is_authenticated:
            self.close()
            return

        self.group_name = f"user_{user.id}"

        # Join personal group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

        # Set online
        presence, _ = UserPresence.objects.get_or_create(user=user)
        presence.set_online()

    def disconnect(self, close_code):
        user = self.scope['user']

        if user.is_authenticated:
            try:
                presence = UserPresence.objects.get(user=user)
                presence.set_offline()
            except UserPresence.DoesNotExist:
                pass

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Home screen message update
    def chat_list_update(self, event):
        self.send(text_data=json.dumps({
            "type": "chat_update",
            "room_name": event["room_name"],
            "message": event["message"],
            "sender_id": event["sender_id"],
            "sender_name": event["sender_name"],
            "timestamp": event["timestamp"]
        }))