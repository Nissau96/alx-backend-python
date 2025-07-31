# messaging/managers.py

from django.db import models
from django.db.models import Q

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to retrieve unread messages for a user.
    """

    def unread_for_user(self, user):
        """
        Returns a queryset of unread messages for a given user.
        """
        return self.get_queryset() \
            .filter(receiver=user, is_read=False) \
            .select_related('sender')