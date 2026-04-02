import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from chat.serializers.utils.massage_notification import send_notification
from .models import ChatMessage, MessageNotificationToken, Conversation
from account.models import UserPresence

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            self.close()
            return

        # ১. Conversation object khunje ber kora
        try:
            self.conversation = Conversation.objects.get(room_name=self.room_name)
        except Conversation.DoesNotExist:
            self.close()
            return

        # ২. গ্রুপে জয়েন করা
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        # ৩. ইউজারকে অনলাইন সেট করা
        presence, _ = UserPresence.objects.get_or_create(user=self.user)
        presence.set_online()

        # ৪. সবাইকে জানানো যে আমি অনলাইন হয়েছি
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'user_status_update',
                'user_id': self.user.id,
                'status': True
            }
        )

        # ৫. প্রিভিয়াস মেসেজ পাঠানো
        self.send_history()

    def disconnect(self, close_code):
        if self.user.is_authenticated:
            try:
                presence = UserPresence.objects.get(user=self.user)
                presence.set_offline()
            except UserPresence.DoesNotExist:
                pass

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_status_update',
                    'user_id': self.user.id,
                    'status': False
                }
            )

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message', '')

        if not self.user.is_authenticated:
            return

        # participants theke onno user-der (friends) online status check kora
        # Note: One-to-One chat er jonno is_read logic eivabe kaj korbe
        friends = self.conversation.participants.exclude(id=self.user.id)
        
        # Simple Logic: At least ekjon friend online thakle is_read True hote pare (depend on your UX)
        is_any_friend_online = UserPresence.objects.filter(user__in=friends, is_online=True).exists()

        # ডাটাবেসে সেভ (Notun Model onujayi)
        new_msg = ChatMessage.objects.create(
            conversation=self.conversation,
            sender=self.user,
            text=message_text,
            is_read=is_any_friend_online
        )

        # Notification pathano shobai ke (Except self)
        for friend in friends:
            self.handle_notification(friend, message_text)
            
            # Protiti friend-er personal group-e chat list update pathano
            async_to_sync(self.channel_layer.group_send)(
                f"user_{friend.id}",
                {
                    "type": "chat_list_update",
                    "room_name": self.room_name,
                    "message": message_text,
                    "sender_id": self.user.id,
                    "sender_name": self.user.first_name,
                    "is_read": is_any_friend_online,
                    "timestamp": str(new_msg.created_at)
                }
            )

        # গ্রুপে মেসেজ ব্রডকাস্টিং
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'user': self.user.id,
                'name': self.user.first_name,
                'timestamp': new_msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'user': event['user'],
            'name': event['name'],
            'timestamp': event['timestamp']
        }))

    def user_status_update(self, event):
        if event['user_id'] != self.user.id:
            self.send(text_data=json.dumps({
                'type': 'status_update',
                'user_id': event['user_id'],
                'active': event['status']
            }))

    def send_history(self):
        previous_messages = self.conversation.messages.all().order_by('created_at')
        for msg in previous_messages:
            self.send(text_data=json.dumps({
                'type': 'history',
                'message': msg.text,
                'user': msg.sender.id,
                'name': msg.sender.first_name,
                'timestamp': msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }))

    def handle_notification(self, friend_user, message):
        try:
            token_obj = MessageNotificationToken.objects.get(user=friend_user)
            send_notification(token_obj.token, self.user.first_name, message)
        except MessageNotificationToken.DoesNotExist:
            pass