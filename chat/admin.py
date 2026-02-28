from django.contrib import admin

# Register your models here.
from chat.models import Connection
@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'friend', 'created_at')
    search_fields = ('user__username', 'friend__username')
    list_filter = ('created_at',)