from datetime import date

from rest_framework import serializers

from .models import UserProfile

VALID_DIETARY = {"vegetarian", "vegan", "gluten_free", "no_restrictions"}


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "full_name",
            "date_of_birth",
            "gender",
            "current_weight_kg",
            "height_cm",
            "target_weight_kg",
            "fitness_goal",
            "activity_level",
            "dietary_preferences",
            "dietary_other_text",
            "health_notes",
            "disclaimer_accepted_at",
            "updated_at",
        ]
        read_only_fields = ["disclaimer_accepted_at", "updated_at"]

    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def validate_dietary_preferences(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Must be a list.")
        invalid = set(value) - VALID_DIETARY
        if invalid:
            raise serializers.ValidationError(f"Invalid values: {sorted(invalid)}")
        return value
