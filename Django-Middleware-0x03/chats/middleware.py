# chats/middleware.py

import logging
from django.utils import timezone

# Get the logger we configured in settings.py
request_logger = logging.getLogger('request_logger')


class RequestLoggingMiddleware:
    """
    Middleware that logs details for every incoming request to a designated log file.
    """

    def __init__(self, get_response):
        """
        Called once by Django during server startup.
        'get_response' is a callable that represents the next middleware or the view.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Called on every request. This is where the main logic resides.
        """

        # If the user is authenticated, request.user will be a User object.
        # If not, it will be an AnonymousUser object.
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log the details using our configured logger
        request_logger.info(
            f"{timezone.now().now().strftime('%Y-%m-%d %H:%M:%S')} - User: {user} - Path: {request.path}"
        )

        # Pass the request to the next middleware or view
        response = self.get_response(request)



        return response