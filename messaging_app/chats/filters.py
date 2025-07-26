# chats/filters.py

import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    """
    FilterSet for the Message model.

    Allows filtering messages by sender, receiver, and a timestamp date range.
    """
    # Define a filter for messages created on or after a specific date.
    # The `lookup_expr='gte'` means "greater than or equal to".
    start_date = django_filters.DateFilter(field_name="timestamp", lookup_expr='gte')

    # Define a filter for messages created on or before a specific date.
    # The `lookup_expr='lte'` means "less than or equal to".
    end_date = django_filters.DateFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = Message
        # Define the fields that can be filtered on directly.
        # This will allow queries like: /api/messages/?sender=1&receiver=2
        fields = ['sender', 'conversation']