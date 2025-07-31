# messaging/models.py

from django.db import models
from django.contrib.auth.models import User


class UnreadMessageManager(models.Manager):
    """
    Custom manager to retrieve unread messages for a user.
    """
    def get_unread_for_user(self, user):
        """
        Returns a queryset of unread messages for a given user,
        optimized to fetch only essential fields.
        """
        return self.get_queryset() \
            .filter(receiver=user, is_read=False) \
            .select_related('sender') \
            .only('id', 'content', 'timestamp', 'sender__username', 'sender__id')

class Message(models.Model):
    """
    Represents a message sent from one user to another.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)

    objects = models.Manager()
    unread = UnreadMessageManager()

    def __str__(self):
        edited_status = "(edited)" if self.is_edited else ""
        if self.parent_message:
            return f"Reply from {self.sender.username} to message {self.parent_message.id} {edited_status}"
        return f"Message from {self.sender.username} to {self.receiver.username} {edited_status}"

# New model to store the history of message edits
class MessageHistory(models.Model):
    """
    Stores the history of edits for a message.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    edited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Order history from newest to oldest
        ordering = ['-edited_at']
        verbose_name_plural = "Message History"

    def __str__(self):
        return f"Edit by {self.edited_by.username} for message {self.message.id} at {self.edited_at:%Y-%m-%d %H:%M}"


class Notification(models.Model):
    """
    Represents a notification for a user about a new message.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} about message from {self.message.sender.username}"

