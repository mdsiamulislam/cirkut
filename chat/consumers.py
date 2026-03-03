import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from chat.serializers.utils.massage_notification import send_notification
from .models import ChatMessage, MessageNotificationToken, Connection
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

        # ১. গ্রুপে জয়েন করা
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        # ২. ইউজারকে অনলাইন সেট করা
        presence, _ = UserPresence.objects.get_or_create(user=self.user)
        presence.set_online()

        # ৩. ফ্রেন্ডকে জানানো যে আমি অনলাইন হয়েছি
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'user_status_update',
                'user_id': self.user.id,
                'status': True
            }
        )

        # ৪. প্রিভিয়াস মেসেজ এবং ফ্রেন্ডের কারেন্ট স্ট্যাটাস পাঠানো
        self.send_history_and_friend_status()

    def disconnect(self, close_code):
        # ১. ইউজারকে অফলাইন সেট করা
        if self.user.is_authenticated:
            try:
                presence = UserPresence.objects.get(user=self.user)
                print("Setting user offline:", self.user.first_name)
                presence.set_offline()
            except UserPresence.DoesNotExist:
                pass

            # ২. ফ্রেন্ডকে জানানো যে আমি অফলাইন হয়েছি
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_status_update',
                    'user_id': self.user.id,
                    'status': False
                }
            )

        # ৩. গ্রুপ ত্যাগ করা
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')

        if not self.user.is_authenticated:
            return

        friend_user = self.get_friend_user()
        is_friend_online = False
        if friend_user:
            try:
                friend_presence = UserPresence.objects.get(user=friend_user)
                is_friend_online = friend_presence.is_online
            except UserPresence.DoesNotExist:
                pass

        # ডাটাবেসে সেভ
        new_msg = ChatMessage.objects.create(
            room_name=self.room_name,
            message=message,
            user=self.user,
            is_read=is_friend_online
        )
        

        # ফ্রেন্ডকে খুঁজে বের করা ও নোটিফিকেশন পাঠানো
        
        if friend_user:
            self.handle_notification(friend_user, message)
            
            friend_id = friend_user.id

            async_to_sync(self.channel_layer.group_send)(
            f"user_{friend_id}", # ফ্রেন্ডের পার্সোনাল গ্রুপে পাঠাচ্ছি
            {
                "friend_id": friend_id,
                "type": "chat_list_update", # UserConsumer-এর মেথডটি কল হবে
                "room_name": self.room_name,
                "message": message,
                "sender_id": self.user.id,
                "sender_name": self.user.first_name,
                'is_read': is_friend_online,
                "timestamp": str(new_msg.timestamp)
            }
        )

        

        # গ্রুপে মেসেজ ব্রডকাস্টিং
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.id,
                'name': self.user.first_name,
                'timestamp': new_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        )

    # --- হ্যান্ডলার মেথডসমূহ ---

    def chat_message(self, event):
        # রিয়েল টাইমে মেসেজ রিসিভ করা
        self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'user': event['user'],
            'name': event['name'],
            'timestamp': event['timestamp']
        }))

    def user_status_update(self, event):
        # ফ্রেন্ড অনলাইন বা অফলাইন হলে এই মেথড কল হবে
        # নিজের স্ট্যাটাস নিজে আপডেট করার দরকার নেই
        if event['user_id'] != self.user.id:
            self.send(text_data=json.dumps({
                'type': 'status_update',
                'active': event['status']
            }))

    def send_history_and_friend_status(self):
        # ফ্রেন্ডের বর্তমান অবস্থা চেক করা
        friend_user = self.get_friend_user()
        is_friend_online = False
        if friend_user:
            try:
                friend_presence = UserPresence.objects.get(user=friend_user)
                is_friend_online = friend_presence.is_online
            except UserPresence.DoesNotExist:
                pass

        # হিস্ট্রি মেসেজ পাঠানো
        previous_messages = ChatMessage.objects.filter(room_name=self.room_name).order_by('timestamp')
        for msg in previous_messages:
            self.send(text_data=json.dumps({
                'type': 'history',
                'message': msg.message,
                'user': msg.user.id,
                'name': msg.user.first_name,
                'active': is_friend_online, # প্রথমবার লোড হওয়ার সময় স্ট্যাটাস
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }))

    def get_friend_user(self):
        try:
            connection = Connection.objects.get(room_name=self.room_name)
            return connection.friend if connection.user == self.user else connection.user
        except Connection.DoesNotExist:
            return None

    def handle_notification(self, friend_user, message):
        try:
            token_obj = MessageNotificationToken.objects.get(user=friend_user)
            send_notification(token_obj.token, self.user.first_name, message)
        except MessageNotificationToken.DoesNotExist:
            pass