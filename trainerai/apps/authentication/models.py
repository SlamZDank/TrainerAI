from typing import final, override
import uuid
from django.db import models

@final
class User(models.Model):
    # finding how to enforce minimum length using django models
    id = models.UUIDField(primary_key = True, default = uuid.uuid7, editable = False)
    email = models.EmailField(unique=True)
    password = models.TextField()
    created_at = models.DateField(auto_now_add = True, editable = False)
    updated_at = models.DateField(auto_now = True)
    onboarding_completed = models.BooleanField(default = False)

    @override
    def __str__(self) -> str:
        return self.id
