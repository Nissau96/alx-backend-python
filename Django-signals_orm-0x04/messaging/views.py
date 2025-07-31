# messaging/views.py
from django.db.models import Prefetch, Q
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message


@login_required
def conversation_view(request):
    """
    Displays top-level messages and their threaded replies efficiently.
    """
    # Filter for top-level messages where the user is either the sender or receiver.
    top_level_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        parent_message__isnull=True
    ) \
        .select_related('sender', 'receiver') \
        .prefetch_related(
        Prefetch(
            'replies',
            queryset=Message.objects.select_related('sender', 'receiver').order_by('timestamp'),
            to_attr='threaded_replies'
        )
    ).order_by('-timestamp')

    context = {
        'messages': top_level_messages
    }
    return render(request, 'messaging/conversation.html', context)

@login_required
def delete_user(request):
    """
    Handles user account deletion.
    - GET: Shows a confirmation page.
    - POST: Deletes the user and all related data.
    """
    if request.method == 'POST':
        user = request.user
        # Log the user out before deleting
        logout(request)
        user.delete()
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('home') # Redirect to a home page or another appropriate page

    return render(request, 'messaging/delete_user_confirm.html')