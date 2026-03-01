import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# 1. Settings set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cirkut.settings')

# 2. Django initialize
django.setup()

# 3. Django setup er por import
from chat.middleware import JwtAuthMiddleware
import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddleware(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})