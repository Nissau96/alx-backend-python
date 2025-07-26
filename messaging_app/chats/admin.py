# messaging_app/chats/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, Message


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the custom User model.
    """
    # Use email instead of username for ordering and display
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')

    # Update fieldsets to use 'email' instead of 'username'
    # This is copied from the default UserAdmin and modified
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password"),
            },
        ),
    )


# Unregister the old UserAdmin if it was somehow registered before
# admin.site.unregister(User) # This line is often not needed but is safe

# Register the User model with the new custom admin class
admin.site.register(User, CustomUserAdmin)

# Register the other models to make them accessible in the admin panel
admin.site.register(Conversation)
admin.site.register(Message)