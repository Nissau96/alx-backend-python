# chats/serializers.py

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    """
    sender = serializers.StringRelatedField()  # Display user's __str__ (email)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model, with nested relationships.
    """
    # Nest the UserSerializer to show full participant details
    participants = UserSerializer(many=True, read_only=True)

    # Nest the MessageSerializer to include all messages within the conversation
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']