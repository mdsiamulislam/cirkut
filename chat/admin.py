from django.contrib import admin

# Register your models here.
from chat.models import Connection, ChatMessage
@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'friend', 'created_at')
    search_fields = ('user__username', 'friend__username')
    list_filter = ('created_at',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_name', 'user', 'message', 'timestamp')
    search_fields = ('room_name', 'user__username', 'message')
    list_filter = ('timestamp',)