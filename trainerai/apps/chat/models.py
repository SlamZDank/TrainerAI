import uuid
from django.db import models
from trainerai.apps.authentication.models import User


class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        to=User, null=False, on_delete=models.CASCADE, related_name="chat_sessions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]


class ChatMessage(models.Model):
    class Role(models.TextChoices):
        USER = "user", "User"
        COACH = "coach", "Coach"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        to=ChatSession, null=False, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=5, choices=Role.choices, null=False)
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
