# messaging_app/chats/views.py

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or edited.
    """
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email', 'participants__first_name']

    def get_queryset(self):
        """
        This view should only return conversations for the currently authenticated user.
        """
        user = self.request.user
        return user.conversations.all()

    def perform_create(self, serializer):
        """
        Create a new conversation and add the current user as a participant.
        """
        # The serializer's validate() method already checks for at least 2 participants.
        # We manually add the requesting user to the list of participants.
        participants = serializer.validated_data.get('participants', [])
        if self.request.user not in participants:
            participants.append(self.request.user)
        serializer.save(participants=participants)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages within a conversation.
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        This view should return a list of all the messages for the conversation
        determined by the conversation_id portion of the URL.
        """
        conversation_id = self.kwargs['conversation_pk']
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        """
        Create a new message, setting the sender and conversation automatically.
        """
        conversation_id = self.kwargs['conversation_pk']
        conversation = Conversation.objects.get(pk=conversation_id)
        # Set the sender to the currently authenticated user.
        serializer.save(sender=self.request.user, conversation=conversation)


from django.shortcuts import render

# Create your views here.
