# chats/filters.py

import django_filters
from django.contrib.auth import get_user_model
from .models import Message

# Get the active User model for this project
User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    """
    FilterSet for the Message model.
    """
    # We explicitly define a 'receiver' filter here.
    # This filter will check for a user within the related conversation's participants.
    receiver = django_filters.ModelChoiceFilter(
        field_name='conversation__participants',
        queryset=User.objects.all(),
        label="Receiver"
    )

    class Meta:
        model = Message
        # The 'fields' list should only contain direct fields on the Message model.
        # Our custom 'receiver' filter is handled above.
        fields = ['sender']