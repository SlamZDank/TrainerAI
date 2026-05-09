from rest_framework import serializers
from .models import ChatSession, ChatMessage, WorkoutPlan, DietPlan


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id", "session", "role", "content", "parts", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_content(self, value):
        parts = self.initial_data.get("parts")
        if parts and len(parts) > 0:
            return value
        if not value or not value.strip():
            raise serializers.ValidationError("Message content cannot be empty.")
        return value


class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ["id", "created_at", "updated_at", "title"]
        read_only_fields = ["id", "created_at", "updated_at"]


class WorkoutPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = ["id", "title", "content", "created_at"]
        read_only_fields = ["id", "created_at"]


class DietPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietPlan
        fields = ["id", "title", "content", "created_at"]
        read_only_fields = ["id", "created_at"]
