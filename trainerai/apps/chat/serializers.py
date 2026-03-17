from rest_framework import serializers
from .models import ChatSession, ChatMessage, WorkoutPlan, DietPlan


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id", "session", "role", "content", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_content(self, value):
        if not value.strip():
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
