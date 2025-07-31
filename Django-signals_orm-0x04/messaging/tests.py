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

    def test_user_data_deleted_on_user_delete(self):
        """
        Test that all user-related data is deleted when a user is deleted.
        """
        # user1 and user2 are created in setUp
        user_to_delete = self.user1
        user_id = user_to_delete.id

        # Create some data for the user
        Message.objects.create(sender=user_to_delete, receiver=self.user2, content="A message")
        self.assertTrue(Message.objects.filter(sender_id=user_id).exists())
        self.assertTrue(Notification.objects.filter(message__sender_id=user_id).exists())

        # Delete the user
        user_to_delete.delete()

        # Check that the user is gone
        self.assertFalse(User.objects.filter(id=user_id).exists())

        # Check that all related data is gone
        self.assertFalse(Message.objects.filter(sender_id=user_id).exists())
        self.assertFalse(Message.objects.filter(receiver_id=user_id).exists())
        self.assertFalse(Notification.objects.filter(user_id=user_id).exists())


class ORMTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='orm_user1', password='password123')
        self.user2 = User.objects.create_user(username='orm_user2', password='password123')

        # Create a conversation thread
        self.msg1 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Main message")
        self.reply1 = Message.objects.create(sender=self.user2, receiver=self.user1, content="Reply 1",
                                             parent_message=self.msg1)
        self.reply2 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Reply to reply 1",
                                             parent_message=self.reply1)

    def test_threaded_view_query_optimization(self):
        """
        Test that the conversation view uses a minimal number of queries.
        """
        # Log in a user to ensure request.user exists for the view's filter
        self.client.login(username='orm_user1', password='password123')

        with self.assertNumQueries(3):
            response = self.client.get('/messaging/conversations/')
            self.assertEqual(response.status_code, 200)


class ManagerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='manager_user1', password='password123')
        self.user2 = User.objects.create_user(username='manager_user2', password='password123')

        # user1 has one unread and one read message
        Message.objects.create(sender=self.user2, receiver=self.user1, content="Unread message", is_read=False)
        Message.objects.create(sender=self.user2, receiver=self.user1, content="Read message", is_read=True)
        # user2 has one unread message
        Message.objects.create(sender=self.user1, receiver=self.user2, content="Another unread message", is_read=False)

    def test_unread_manager_returns_correct_messages(self):
        """
        Test that the UnreadMessageManager returns only unread messages for a user.
        """
        # Get unread messages for user1
        unread_for_user1 = Message.unread.get_unread_for_user(self.user1)

        # Check counts
        self.assertEqual(unread_for_user1.count(), 1)
        self.assertEqual(Message.objects.filter(receiver=self.user1, is_read=True).count(), 1)

        # Check content
        self.assertEqual(unread_for_user1.first().content, "Unread message")

        # Check that it doesn't return messages for other users
        self.assertNotIn("Another unread message", [m.content for m in unread_for_user1])