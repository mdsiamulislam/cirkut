from django.urls import path
from chat.views.connection_view import ConnectionListView, NotificationTestView
from chat.views.notification_view import NotificationRegisterView
from chat.views.latest_chat_view import LatestChatView
from chat.views.chat_list_view import ChatListView

urlpatterns = [
    path('connections/', ConnectionListView.as_view(), name='connections'),
    path('test-notification/', NotificationTestView.as_view(), name='test-notification'),

    path('register-notification/', NotificationRegisterView.as_view(), name='register-notification'),
    path('latest-chat/', LatestChatView.as_view(), name='latest-chat'),
    path('chat-list/', ChatListView.as_view(), name='chat-list'),
]
