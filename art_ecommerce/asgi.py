import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

import chat
import store
from chat.consumers import ChatConsumer
from store.consumers import BidConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/accounts/dashboard/chat_history/<slug:room_id>/', chat.consumers.ChatConsumer.as_asgi()),
            path('ws/<genre_slug>/<artwork_slug>/place_bid/', store.consumers.BidConsumer.as_asgi()),
        ])
    )
})
