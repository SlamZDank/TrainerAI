from django.urls import path
from . import views

urlpatterns = [
    path("chat/sessions/", views.ChatSessionListCreateView.as_view(), name="chat-sessions"),
    path("chat/sessions/<uuid:session_id>/", views.ChatSessionDetailView.as_view(), name="chat-session-detail"),
    path("chat/sessions/<uuid:session_id>/messages/", views.ChatMessageListCreateView.as_view(), name="chat-messages"),
    path("chat/workout-plans/", views.WorkoutPlanListCreateView.as_view(), name="workout-plans"),
    path("chat/diet-plans/", views.DietPlanListCreateView.as_view(), name="diet-plans"),
]
