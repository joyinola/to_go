from django.db import models
from rideshare.models import User

# Create your models here.


class Chat(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_1")
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_2")

    class Meta:
        unique_together = ("user_1", "user_2")


class Messages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # unread = models.BooleanField(default=False)
    class Meta:
        ordering = ["created_at"]
