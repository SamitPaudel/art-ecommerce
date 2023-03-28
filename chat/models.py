from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from store.models import Artwork


class ChatRoom(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    members = models.ManyToManyField(get_user_model())
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artwork.artwork_title} - {', '.join([user.username for user in self.members.all()])}"


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.name} -> {self.receiver.name}: {self.message}"
