# messaging/admin.py

from django.contrib import admin
from .models import Message, Notification, MessageHistory

# An inline admin to show history directly on the message page
class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ('old_content', 'timestamp') # Make history read-only

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'is_edited', 'timestamp')
    list_filter = ('timestamp', 'sender', 'receiver', 'is_edited')
    inlines = [MessageHistoryInline]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'timestamp')
    list_filter = ('is_read', 'timestamp', 'user')


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'old_content', 'timestamp')
    list_filter = ('timestamp',)