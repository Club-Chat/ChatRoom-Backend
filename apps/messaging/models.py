from django.conf import settings
from django.db import models
from apps.chat.models import Room

User = settings.AUTH_USER_MODEL


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')

    content = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.id} from {self.sender}"


class MessageReadStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='read_statuses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('message', 'user')

    def __str__(self):
        return f"{self.user} read Message {self.message.id}"