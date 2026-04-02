from django.urls import path

#Connection views
from connection.views.connections import ConnectionsView, ConnectionActionView
from connection.views.connection_request_view import ConnectionRequestView, ConnectionRequestActionView

#Conversation views
from chat.views.conversation_view import ConversationListView

urlpatterns = [
    path('v1/connections/', ConnectionsView.as_view(), name='connections'),
    path('v1/connections/<int:connection_id>/', ConnectionActionView.as_view(), name='delete-connection'),
    path('v1/received-requests/', ConnectionRequestView.as_view(), name='connection-requests'),
    path('v1/received-requests/<int:request_id>/', ConnectionRequestActionView.as_view(), name='accept-connection-request'),


    # Conversation APIs
    path('v1/conversations/', ConversationListView.as_view(), name='conversation-list'),
]
