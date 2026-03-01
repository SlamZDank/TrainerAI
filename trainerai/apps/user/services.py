from django.db import transaction

from trainerai.apps.authentication.models import User
from .models import UserProfile

# figure out how to jwt in djangorestframework
@transaction.atomic
def create_user_profile(user: User, validated_data):
    profile = UserProfile.objects.create(user = user, **validated_data)
    user.onboarding_completed = True
    user.save(update_fields=["onboarding_completed"])
    return profile

