from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from artist.models import Artist
from store.models import Artwork


class ChatRoom(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_rooms')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist_rooms')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'artist', 'artwork']

    def __str__(self):
        return f'ChatRoom between {self.user} and {self.artist} about {self.artwork}'

    def get_messages(self):
        return self.messages.order_by('-date_sent')


class ChatMessage(models.Model):
    """
    Represents a message sent in a chat room.
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} in ChatRoom({self.room.pk})'

    def save(self, *args, **kwargs):
        super(ChatMessage, self).save(*args, **kwargs)
