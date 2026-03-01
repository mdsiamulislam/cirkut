from django.urls import path
from chat.views.connection_view import ConnectionListView, NotificationTestView
from chat.views.notification_view import NotificationRegisterView

urlpatterns = [
    path('connections/', ConnectionListView.as_view(), name='connections'),
    path('test-notification/', NotificationTestView.as_view(), name='test-notification'),

    path('register-notification/', NotificationRegisterView.as_view(), name='register-notification'),
]
