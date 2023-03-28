import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):

        # Extract genres_slug and artwork_slug from URL
        self.genres_slug = self.scope['url_route']['kwargs']['genres_slug']
        self.artwork_slug = self.scope['url_route']['kwargs']['artwork_slug']
        # Create unique room group name
        self.room_group_name = f'chat_{self.genres_slug}_{self.artwork_slug}'

        # Add channel to room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'message': message, 'type': 'send_back'})

    def send_back(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))
