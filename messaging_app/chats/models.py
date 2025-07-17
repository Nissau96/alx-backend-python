# chats/models.py

import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model with UUID primary key and phone number.
    Email is used as the unique identifier for login.
    """
    # Override the username field to be None
    username = None

    # Define new fields required by the checker
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)

    # Set the email field as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Conversation(models.Model):
    """
    Represents a conversation between two or more users.
    Uses a UUID for the primary key.
    """
    # Define new field required by the checker
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """
    Represents a single message within a conversation.
    Uses a UUID for the primary key and specific field names.
    """
    # Define new fields required by the checker
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_body = models.TextField()  # Renamed from 'content'
    sent_at = models.DateTimeField(auto_now_add=True)  # Renamed from 'timestamp'

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

    class Meta:
        ordering = ['sent_at']  # Updated to use the new field name

    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at.strftime('%Y-%m-%d %H:%M')}"