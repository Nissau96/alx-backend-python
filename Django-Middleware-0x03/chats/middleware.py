# chats/middleware.py

import logging
import time
from datetime import time as dt_time

from django.core import cache
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone

# Get the logger we configured in settings.py
request_logger = logging.getLogger('request_logger')


class RequestLoggingMiddleware:
    """
    Middleware that logs details for every incoming request to a designated log file.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"

        # FIX: Removed the extra .now() call
        request_logger.info(
            f"{timezone.now().strftime('%Y-%m-%d %H:%M:%S')} - User: {user} - Path: {request.path}"
        )

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Restricts access to the application to a specific time window.
    Allows access between 9:00 AM and 6:00 PM (18:00).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time(9, 0)
        end_time = time(18, 0)
        current_time = timezone.now().time()

        if not (start_time <= current_time <= end_time):
            # FIX: Added the missing closing parenthesis ')'
            return HttpResponseForbidden("Access is restricted to between 9 AM and 6 PM.")

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Limits the number of POST requests an IP address can make to 5 per minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # We only want to rate-limit POST requests for sending messages
        if request.method != 'POST':
            return self.get_response(request)

        # Get the client's IP address
        ip_address = self.get_client_ip(request)
        if not ip_address:
            # If we can't get the IP, let the request pass
            return self.get_response(request)

        # Define the limits
        REQUEST_LIMIT = 5
        TIME_WINDOW = 60  # seconds

        # Use the IP address as the cache key
        cache_key = f"rate_limit_{ip_address}"

        # Get the list of recent request timestamps from the cache
        request_timestamps = cache.get(cache_key, [])

        # Get the current time
        current_time = time.time()

        # Filter out timestamps that are outside the time window
        recent_timestamps = [ts for ts in request_timestamps if current_time - ts < TIME_WINDOW]

        # If the user has exceeded the limit, return a 429 error
        if len(recent_timestamps) >= REQUEST_LIMIT:
            return JsonResponse(
                {'error': 'Rate limit exceeded. Please try again later.'},
                status=429  # 429 Too Many Requests
            )

        # Add the current timestamp and save it back to the cache
        recent_timestamps.append(current_time)
        cache.set(cache_key, recent_timestamps, TIME_WINDOW)

        # Allow the request to proceed
        return self.get_response(request)

    def get_client_ip(self, request):
        """Helper function to get the client's real IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolepermissionMiddleware:
    """
    Restricts access to specified paths based on user role.
    Only allows users with 'is_staff' or 'is_superuser' flags to access '/admin/'.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # We only want to apply this check to paths starting with /admin/
        if request.path.startswith('/admin/'):
            # The AuthenticationMiddleware must run before this, so request.user exists.
            if not request.user.is_authenticated:
                # If the user is not logged in, they will be redirected by other logic.
                # We can let the request pass to the next middleware.
                return self.get_response(request)

            # Check if the authenticated user is staff or a superuser.
            if not (request.user.is_staff or request.user.is_superuser):
                # If not, deny access.
                return HttpResponseForbidden("You do not have permission to access this page.")

        # For all other paths, or for authorized users, let the request proceed.
        return self.get_response(request)