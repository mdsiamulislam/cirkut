from django.contrib import admin

# Register your models here.
from chat.models import Connection, ChatMessage, Conversation, MessageNotificationToken

admin.site.register(Connection)
admin.site.register(ChatMessage)
admin.site.register(Conversation)
admin.site.register(MessageNotificationToken)

