# messaging/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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