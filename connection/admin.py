from django.contrib import admin
from .models.user_connection_model import ConnectionRequest
# Register your models here.

admin.site.register(ConnectionRequest)
