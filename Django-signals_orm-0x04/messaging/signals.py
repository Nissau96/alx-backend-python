# messaging/signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Creates a notification when a new message is saved.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
        print(f"Notification created for {instance.receiver.username}")

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before a message is saved, check if its content has changed.
    If so, log the old content to MessageHistory.
    """

    if instance.pk is None:
        return

    try:
        # Get the original message from the database
        original_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        # Should not happen if instance.pk is not None, but good practice
        return

    # Compare the content from the database with the content about to be saved
    if original_message.content != instance.content:
        # Content has changed, so create a history record
        MessageHistory.objects.create(
            message=original_message,
            old_content=original_message.content
        )
        # Mark the message instance as edited
        instance.is_edited = True