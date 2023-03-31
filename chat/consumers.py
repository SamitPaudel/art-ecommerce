import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels_redis.core import logger

from chat.models import ChatMessage, ChatRoom


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = 'chat_' + self.room_id
        async_to_sync(self.channel_layer.group_add)(self.room_group_id, self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_id, self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        room = ChatRoom.objects.get(id=self.room_id)
        chat_message = ChatMessage.objects.create(sender=user, room=room, content=message)
        async_to_sync(self.channel_layer.group_send)(self.room_group_id, {'message': message, 'type': 'send_back'})

    def send_back(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))
