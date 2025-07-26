"""
Custom permissions for the messaging app.
Ensures users can only access their own messages and conversations.
"""

from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users and participants 
    in a conversation to send, view, update and delete messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users to access the API
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Handle different HTTP methods for conversation participation
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            # For conversation objects
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()

            # For message objects, check the related conversation
            if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
                return request.user in obj.conversation.participants.all()

        return False


class IsParticipantForMessages(permissions.BasePermission):
    """
    Specific permission class for message operations.
    Ensures only conversation participants can send, view, update and delete messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check authentication
        if not request.user or not request.user.is_authenticated:
            return False

        # Handle all HTTP methods for message operations
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            # For message objects
            if hasattr(obj, 'conversation'):
                # Check if user is a participant in the conversation
                is_participant = request.user in obj.conversation.participants.all()

                # For PUT, PATCH, DELETE operations, also check if user is the message sender
                if request.method in ['PUT', 'PATCH', 'DELETE']:
                    return is_participant and (obj.sender == request.user)

                # For GET and POST operations, just check participation
                return is_participant

        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Handles GET, POST, PUT, PATCH, DELETE methods appropriately.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are granted for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions (POST, PUT, PATCH, DELETE) are only allowed to the owner of the object.
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return obj.owner == request.user

        return False


class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    Handles all HTTP methods: GET, POST, PUT, PATCH, DELETE.
    """

    def has_object_permission(self, request, view, obj):
        # Check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Handle all HTTP methods
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            # Check if the user is a participant in the conversation
            return request.user in obj.participants.all()

        return False


class IsMessageOwnerOrConversationParticipant(permissions.BasePermission):
    """
    Custom permission to allow message owners or conversation participants to access messages.
    Handles GET, POST, PUT, PATCH, DELETE operations with different access levels.
    """

    def has_object_permission(self, request, view, obj):
        # Check authentication
        if not request.user or not request.user.is_authenticated:
            return False

        # Handle different HTTP methods
        if request.method in ['GET', 'POST']:
            # Allow message owner to access/view their message
            if hasattr(obj, 'sender') and obj.sender == request.user:
                return True

            # Allow conversation participants to view messages
            if hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()

        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            # Only allow message owner to modify/delete their messages
            if hasattr(obj, 'sender') and obj.sender == request.user:
                # Also ensure they're still a participant in the conversation
                if hasattr(obj, 'conversation'):
                    return request.user in obj.conversation.participants.all()
                return True

        return False


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    Handles GET, POST, PUT, PATCH, DELETE methods.
    """

    def has_object_permission(self, request, view, obj):
        # Check authentication
        if not request.user or not request.user.is_authenticated:
            return False

        # Handle all HTTP methods
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            # Check if the object has an 'owner' field
            if hasattr(obj, 'owner'):
                return obj.owner == request.user

            # Check if the object has a 'user' field
            if hasattr(obj, 'user'):
                return obj.user == request.user

            # Check if the object has a 'sender' field (for messages)
            if hasattr(obj, 'sender'):
                return obj.sender == request.user

        return False


class CanAccessConversation(permissions.BasePermission):
    """
    Permission class to check if user can access a conversation.
    Users can access conversations they are participants in.
    Handles all HTTP methods: GET, POST, PUT, PATCH, DELETE.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check authentication
        if not request.user or not request.user.is_authenticated:
            return False

        # Handle all HTTP methods
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            # For conversation objects
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()

            # For message objects, check the related conversation
            if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
                return request.user in obj.conversation.participants.all()

        return False


class CanAccessMessage(permissions.BasePermission):
    """
    Permission class to check if user can access a message.
    Users can access messages in conversations they participate in.
    Handles different permissions for GET, POST, PUT, PATCH, DELETE.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check authentication
        if not request.user or not request.user.is_authenticated:
            return False

        # Handle different HTTP methods
        if request.method in ['GET', 'POST']:
            # Check if user is the sender of the message
            if hasattr(obj, 'sender') and obj.sender == request.user:
                return True

            # Check if user is a participant in the conversation
            if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
                return request.user in obj.conversation.participants.all()

        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            # Only message sender can modify/delete messages
            if hasattr(obj, 'sender') and obj.sender == request.user:
                # Also verify they're still a conversation participant
                if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
                    return request.user in obj.conversation.participants.all()
                return True

        return False


class IsAuthenticatedAndOwner(permissions.BasePermission):
    """
    Combines authentication check with ownership verification.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Multiple ownership checks for different object types
        ownership_fields = ['owner', 'user', 'sender', 'created_by']

        for field in ownership_fields:
            if hasattr(obj, field):
                field_value = getattr(obj, field)
                if field_value == request.user:
                    return True

        # Special case for conversations - check participants
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        return False


# Utility functions for permission checking
def user_can_access_conversation(user, conversation):
    """
    Helper function to check if a user can access a conversation.

    Args:
        user: The user to check permissions for
        conversation: The conversation object

    Returns:
        bool: True if user can access the conversation, False otherwise
    """
    if not user or not user.is_authenticated:
        return False

    return user in conversation.participants.all()


def user_can_access_message(user, message):
    """
    Helper function to check if a user can access a message.

    Args:
        user: The user to check permissions for
        message: The message object

    Returns:
        bool: True if user can access the message, False otherwise
    """
    if not user or not user.is_authenticated:
        return False

    # User is the sender
    if message.sender == user:
        return True

    # User is a participant in the conversation
    if hasattr(message, 'conversation'):
        return user in message.conversation.participants.all()

    return False


def user_owns_object(user, obj):
    """
    Helper function to check if a user owns an object.

    Args:
        user: The user to check ownership for
        obj: The object to check ownership of

    Returns:
        bool: True if user owns the object, False otherwise
    """
    if not user or not user.is_authenticated:
        return False

    # Check common ownership fields
    ownership_fields = ['owner', 'user', 'sender', 'created_by']

    for field in ownership_fields:
        if hasattr(obj, field):
            field_value = getattr(obj, field)
            if field_value == user:
                return True

    return False