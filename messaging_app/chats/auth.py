"""
Authentication views and utilities for the messaging app.
Handles JWT token generation, user authentication, and related functionality.
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

import json
import logging

logger = logging.getLogger(__name__)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to add additional user information to JWT tokens.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff
        token['is_active'] = user.is_active

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra responses
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'is_staff': self.user.is_staff,
            'is_active': self.user.is_active,
        }

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view with additional user information.
    """
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):
    """
    User registration view with JWT token generation.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data

            # Extract user data
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')

            # Validate required fields
            if not username or not email or not password:
                return Response({
                    'error': 'Username, email, and password are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return Response({
                    'error': 'Username already exists'
                }, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({
                    'error': 'Email already exists'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate password
            try:
                validate_password(password)
            except ValidationError as e:
                return Response({
                    'error': 'Password validation failed',
                    'details': list(e.messages)
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create user
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                first_name=first_name,
                last_name=last_name
            )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Log successful registration
            logger.info(f"New user registered: {username}")

            return Response({
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(access_token),
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return Response({
                'error': 'Registration failed',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    """
    Logout view that blacklists the refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')

            if not refresh_token:
                return Response({
                    'error': 'Refresh token is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()

            logger.info(f"User logged out: {request.user.username}")

            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return Response({
                'error': 'Logout failed',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    View to get and update user profile information.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user's profile information."""
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
        })

    def put(self, request):
        """Update current user's profile information."""
        try:
            user = request.user
            data = request.data

            # Update allowed fields
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'email' in data:
                # Check if email already exists for another user
                if User.objects.filter(email=data['email']).exclude(id=user.id).exists():
                    return Response({
                        'error': 'Email already exists'
                    }, status=status.HTTP_400_BAD_REQUEST)
                user.email = data['email']

            user.save()

            logger.info(f"User profile updated: {user.username}")

            return Response({
                'message': 'Profile updated successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })

        except Exception as e:
            logger.error(f"Profile update error: {str(e)}")
            return Response({
                'error': 'Profile update failed',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    View to change user password.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            data = request.data

            old_password = data.get('old_password')
            new_password = data.get('new_password')

            if not old_password or not new_password:
                return Response({
                    'error': 'Both old and new passwords are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check old password
            if not user.check_password(old_password):
                return Response({
                    'error': 'Old password is incorrect'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate new password
            try:
                validate_password(new_password, user)
            except ValidationError as e:
                return Response({
                    'error': 'New password validation failed',
                    'details': list(e.messages)
                }, status=status.HTTP_400_BAD_REQUEST)

            # Update password
            user.set_password(new_password)
            user.save()

            logger.info(f"Password changed for user: {user.username}")

            return Response({
                'message': 'Password changed successfully'
            })

        except Exception as e:
            logger.error(f"Password change error: {str(e)}")
            return Response({
                'error': 'Password change failed',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


# Utility functions for authentication
def get_tokens_for_user(user):
    """
    Generate JWT tokens for a user.

    Args:
        user: User instance

    Returns:
        dict: Dictionary containing refresh and access tokens
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def authenticate_user(username, password):
    """
    Authenticate user with username and password.

    Args:
        username: Username string
        password: Password string

    Returns:
        User instance if authentication successful, None otherwise
    """
    try:
        user = authenticate(username=username, password=password)
        return user
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return None


def is_user_authenticated(request):
    """
    Check if the request contains a valid JWT token.

    Args:
        request: Django request object

    Returns:
        bool: True if user is authenticated, False otherwise
    """
    try:
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(
            jwt_auth.get_raw_token(jwt_auth.get_header(request))
        )
        user = jwt_auth.get_user(validated_token)
        return user is not None and user.is_authenticated
    except Exception:
        return False


def get_user_from_token(request):
    """
    Extract user from JWT token in request.

    Args:
        request: Django request object

    Returns:
        User instance if token is valid, None otherwise
    """
    try:
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(
            jwt_auth.get_raw_token(jwt_auth.get_header(request))
        )
        user = jwt_auth.get_user(validated_token)
        return user
    except Exception:
        return None


# Decorators for authentication
def jwt_required(view_func):
    """
    Decorator to require JWT authentication for a view.
    """

    def wrapper(request, *args, **kwargs):
        if not is_user_authenticated(request):
            return JsonResponse({
                'error': 'Authentication required'
            }, status=401)
        return view_func(request, *args, **kwargs)

    return wrapper


# API Views for testing authentication
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    """
    Protected view that requires authentication.
    """
    return Response({
        'message': 'This is a protected view',
        'user': request.user.username
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def public_view(request):
    """
    Public view that doesn't require authentication.
    """
    return Response({
        'message': 'This is a public view'
    })