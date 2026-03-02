import uuid
from typing import final
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from trainerai.apps.authentication.models import User

@final
class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class GenderChoices(models.TextChoices):
        MALE = "Male"
        FEMALE = "Female"
        PREFER_NOT = "Prefer not to say"

    class FitnessGoalChoices(models.TextChoices):
        LOSE_WEIGHT = "lostWeight"
        BUILD_MUSCLE = "buildMuscle"
        IMPROVE_ENDURANCE = "improveEndurance"
        GENERAL_WELLNESS = "generalWellness"

    class ActivityLevelChoices(models.TextChoices):
        SEDENTARY = "sedentary"
        LIGHTLY_ACTIVE = "lightlyActive"
        MODERATELY_ACTIVE = "moderatelyActive"
        VERY_ACTIVE = "veryActive"

    user =  models.OneToOneField(to = User, null = False,on_delete = models.CASCADE)
    full_name = models.CharField(max_length = 255, null = False, blank = False)
    date_of_birth = models.DateField(null = False)
    gender = models.CharField(max_length = 20,choices = GenderChoices, null = False)
    current_weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null = True, validators=[MinValueValidator(20), MaxValueValidator(500)])
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null = True, validators=[MinValueValidator(50), MaxValueValidator(300)])
    target_weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null = True, validators=[MinValueValidator(20), MaxValueValidator(500)])
    fitness_goal = models.CharField(max_length = 20, choices = FitnessGoalChoices.choices)
    activity_level = models.CharField(max_length = 20, choices = ActivityLevelChoices.choices)
    dietary_preferences = models.JSONField()
    dietary_other_text = models.CharField(max_length = 500, blank = True)
    disclaimer_accepted_at = models.DateTimeField(null = False)
    updated_at = models.DateTimeField(auto_now = True)

# - current_weight_kg and target_weight_kg MUST be in range [20, 500].
# - height_cm MUST be in range [50, 300].
# - dietary_preferences MUST only contain values from the recognised list.
# - dietary_other_text is only meaningful when dietary_preferences contains 'other'.
# - disclaimer_accepted_at MUST be set on profile creation (enforced at the API layer).
# - Creating a UserProfile MUST atomically set user.onboarding_completed = True
