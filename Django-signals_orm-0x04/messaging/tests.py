# messaging/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


class SignalsTestCase(TestCase):
    def setUp(self):
        """Set up test users."""
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original content."
        )

    def test_notification_created_on_new_message(self):
        """
        Test that a notification is created when a new message is sent.
        """
        initial_notification_count = Notification.objects.count()

        # Create a new message from user1 to user2
        new_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello, this is a test!"
        )

        # Check that one new notification has been created
        self.assertEqual(Notification.objects.count(), initial_notification_count + 1)

        # Ensure no notifications exist initially for user2
        self.assertEqual(Notification.objects.count(), 0)

        # Create a new message from user1 to user2
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello, this is a test!"
        )

        # Check that one notification has been created
        self.assertEqual(Notification.objects.count(), 1)

        # Check that the notification is for the correct user and message
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)

    def test_history_logged_on_message_edit(self):
        """
        Test that message history is logged when a message is edited.
        """
        # Ensure no history exists initially
        self.assertEqual(MessageHistory.objects.count(), 0)
        self.assertFalse(self.message.is_edited)

        # 1. Edit the message content and save
        original_content = self.message.content
        self.message.content = "Edited content."
        self.message.save()

        # 2. Check that one history record was created
        self.assertEqual(MessageHistory.objects.count(), 1)
        history_record = MessageHistory.objects.first()
        self.assertEqual(history_record.message, self.message)
        self.assertEqual(history_record.old_content, original_content)

        # 3. Check that the message is now marked as edited
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_edited)

        # 4. Save again without changes, ensure no new history is created
        self.message.save()
        self.assertEqual(MessageHistory.objects.count(), 1)