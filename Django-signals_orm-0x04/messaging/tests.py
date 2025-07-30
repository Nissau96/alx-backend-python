# messaging/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalsTestCase(TestCase):
    def setUp(self):
        """Set up test users."""
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

    def test_notification_created_on_new_message(self):
        """
        Test that a notification is created when a new message is sent.
        """
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