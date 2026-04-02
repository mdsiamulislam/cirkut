from django.contrib import admin

# Register your models here.
from chat.models import Connection, ChatMessage, Conversation, GroupChat
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

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
    filter_horizontal = ('participants',)

@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'room_name', 'created_at')
    search_fields = ('name', 'room_name')