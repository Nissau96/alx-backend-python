# chats/views.py

"""
Views for the messaging app with proper authentication and permissions.
"""
import logging

from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Max
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter

from .models import Conversation, Message, MessageReadStatus
# The key custom permission class for this task
from .permissions import IsParticipantOfConversation
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    ConversationDetailSerializer,
    MessageDetailSerializer
)


# Standard setup for logging and getting the User model
logger = logging.getLogger(__name__)
User = get_user_model()


class ChatPagination(PageNumberPagination):
    """Custom pagination for chat views."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationDetailSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = ChatPagination

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user
        ).annotate(
            last_message_time=Max('messages__created_at'),
            message_count=Count('messages')
        ).order_by('-last_message_time')

    def perform_create(self, serializer):
        conversation = serializer.save(created_by=self.request.user)
        conversation.participants.add(self.request.user)

    def perform_update(self, serializer):
        conversation = self.get_object()
        if conversation.created_by != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied('You do not have permission to update this conversation.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.created_by != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied('You do not have permission to delete this conversation.')
        instance.delete()


class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific conversation.
    """
    serializer_class = ConversationDetailSerializer
    # Permissions: User must be authenticated and a participant of this specific conversation.
    # The `IsParticipantOfConversation` class will check this for GET, PUT, PATCH, DELETE.
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """Return conversations where the user is a participant."""
        return Conversation.objects.filter(participants=self.request.user)

    def perform_update(self, serializer):
        """Adds a finer-grained check: only the creator or staff can update details."""
        conversation = self.get_object()
        if conversation.created_by != self.request.user and not self.request.user.is_staff:
            logger.warning(f"Unauthorized update attempt on conversation {conversation.id} by {self.request.user.username}")
            raise PermissionDenied('You do not have permission to modify this conversation.')
        serializer.save()
        logger.info(f"Conversation {conversation.id} updated by {self.request.user.username}")

    def perform_destroy(self, instance):
        """Adds a finer-grained check: only the creator or staff can delete the conversation."""
        if instance.created_by != self.request.user and not self.request.user.is_staff:
            logger.warning(f"Unauthorized delete attempt on conversation {instance.id} by {self.request.user.username}")
            raise PermissionDenied('You do not have permission to delete this conversation.')
        logger.info(f"Conversation {instance.id} deleted by {self.request.user.username}")
        instance.delete()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageDetailSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = ChatPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        user_conversations = Conversation.objects.filter(participants=self.request.user)
        return Message.objects.filter(
            conversation__in=user_conversations
        ).select_related('sender', 'conversation').order_by('-created_at')

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied('You are not a participant in this conversation.')
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        message = self.get_object()
        if message.sender != self.request.user:
            raise PermissionDenied('You can only edit your own messages.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.sender != self.request.user:
            raise PermissionDenied('You can only delete your own messages.')
        instance.delete()



class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific message.
    """
    serializer_class = MessageDetailSerializer
    # Permissions: User must be authenticated and a participant in the message's conversation.
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        The queryset is already secure. It only includes messages from conversations
        the user is a part of.
        """
        user_conversations = Conversation.objects.filter(participants=self.request.user)
        return Message.objects.filter(conversation__in=user_conversations)

    def perform_update(self, serializer):
        """Finer-grained check: Only the original sender can edit their message."""
        message = self.get_object()
        if message.sender != self.request.user:
            logger.warning(f"User {self.request.user.username} tried to update message {message.id} they don't own.")
            raise PermissionDenied('You can only edit your own messages.')
        serializer.save()

    def perform_destroy(self, instance):
        """Finer-grained check: Only the original sender can delete their message."""
        if instance.sender != self.request.user:
            logger.warning(f"User {self.request.user.username} tried to delete message {instance.id} they don't own.")
            raise PermissionDenied('You can only delete your own messages.')
        instance.delete()


# The following views are for listing user-specific data and do not need the
# IsParticipantOfConversation permission class, as they don't operate on a
# single, specific conversation object that needs to be checked. IsAuthenticated is sufficient.

class UserConversationsView(generics.ListAPIView):
    """List all conversations for the currently authenticated user."""
    serializer_class = ConversationDetailSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ChatPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        # The logic is inherently secure as it's filtered by `request.user`.
        return Conversation.objects.filter(
            participants=self.request.user
        ).annotate(
            last_message_time=Max('messages__created_at')
        ).order_by('-last_message_time')


class MessageSearchView(generics.ListAPIView):
    """Search messages across all of the user's conversations."""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ChatPagination

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if not query:
            return Message.objects.none()

        # The query is securely filtered to only search within the user's conversations.
        user_conversations = Conversation.objects.filter(participants=self.request.user)
        return Message.objects.filter(
            conversation__in=user_conversations,
            content__icontains=query
        ).select_related('sender').order_by('-created_at')