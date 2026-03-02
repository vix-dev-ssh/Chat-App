from django.db import models
from django.conf import settings

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey( #ForeignKey is the Link. It tells the database that this message belongs to a specific user
        settings.AUTH_USER_MODEL, #tells Django to link the message to your custom User model
        on_delete=models.CASCADE, #If a user deletes their account, all messages they sent or received will be automatically deleted too
        related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )
    content = models.TextField() #stores the actual text of the chat
    timestamp = models.DateTimeField(auto_now_add=True) #automatically records the exact second the message was created
    is_read = models.BooleanField(default=False) #starts as False (unread) and you can flip it to True once the receiver opens the chat

    def __str__(self):
        return f"{self.sender} -> {self.receiver}" #you will see a clear summary like: a@email.com -> b@email.com