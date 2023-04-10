import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels_redis.core import logger

from chat.models import ChatMessage, ChatRoom


class BidConsumer(WebsocketConsumer):
    def connect(self):
        pass

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        pass