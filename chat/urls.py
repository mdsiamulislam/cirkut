from django.urls import path
from chat.views.connection_view import ConnectionListView

urlpatterns = [
    path('connections/', ConnectionListView.as_view(), name='connections'),
]
