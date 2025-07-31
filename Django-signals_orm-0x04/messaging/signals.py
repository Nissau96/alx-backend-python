# messaging/signals.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save, pre_delete
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

        return

    # Compare the content from the database with the content about to be saved
    if original_message.content != instance.content:
        
        MessageHistory.objects.create(
            message=original_message,
            old_content=original_message.content
        )
        # Mark the message instance as edited
        instance.is_edited = True


@receiver(pre_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    Before a user is deleted, clean up all their related data.

    """
    user = instance
    print(f"User {user.username} is being deleted. Cleaning up related data...")

    # Delete messages where the user is either a sender or receiver
    Message.objects.filter(models.Q(sender=user) | models.Q(receiver=user)).delete()



    print(f"Cleanup for user {user.username} complete.")