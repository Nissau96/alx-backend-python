# chats/middleware.py

import logging
from datetime import time
from django.http import HttpResponseForbidden
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


# FIX: This class was moved out from inside the class above.
# It must be a separate, top-level class.
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