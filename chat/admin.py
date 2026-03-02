from django.contrib import admin
from .models import Message

# Register your models here.

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "content", "timestamp", "is_read")
    list_filter = ("is_read", "timestamp")
    search_fields = ("content",)