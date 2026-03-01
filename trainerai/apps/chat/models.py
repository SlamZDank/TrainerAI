import uuid
from django.db import models
from trainerai.apps.authentication.models import User

# Create your models here.
class ChatSession(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid7, editable = False)
    user = models.ForeignKey(to = User, null = False, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class ChatMessage(models.Model):
    class ChatRoleChoice(models.TextChoices):
        USER = "USER"
        AI = "AI"

    id = models.UUIDField(primary_key = True, default = uuid.uuid7, editable = False)
    session = models.ForeignKey(to = ChatSession, null = False, on_delete = models.CASCADE)
    role = models.TextField(max_length = 6, choices = ChatRoleChoice.choices, null = False)
    content = models.TextField(max_length = 5000, blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add = True)
