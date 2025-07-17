# chats/models.py

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    This allows for future customization if needed.
    """
    pass


class Conversation(models.Model):
    """
    Represents a conversation between two or more users.
    """
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    Represents a single message within a conversation.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"