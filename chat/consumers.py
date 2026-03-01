import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .models import ChatMessage

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        is_authenticated = self.scope['user'].is_authenticated
        if not is_authenticated:
            self.close()
            return
        self.accept()

        # Previous messages fetch kora
        previous_messages = ChatMessage.objects.filter(room_name=self.room_name).order_by('timestamp')
        for msg in previous_messages:
            self.send(text_data=json.dumps({
                'message': msg.message,
                'user': msg.user.id,
                'name': msg.user.first_name,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        user = self.scope['user']

        if user.is_anonymous:
            self.send(text_data=json.dumps({
                'error': 'Unauthorized'
            }))
            return

        # Database e save
        new_msg = ChatMessage.objects.create(
            room_name=self.room_name,
            message=message,
            user=user
        )

        # Group e send
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.id,
                'name': user.first_name,
                'timestamp': new_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        )
    def chat_message(self, event):
        # WebSocket-e message pathano
        self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
            'name': event['name'],
            'timestamp': event['timestamp']
        }))