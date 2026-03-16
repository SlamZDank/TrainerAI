from django.urls import path
from . import views

urlpatterns = [
    path("chat/sessions/", views.ChatSessionListCreateView.as_view(), name="chat-sessions"),
    path("chat/sessions/<uuid:session_id>/", views.ChatSessionDetailView.as_view(), name="chat-session-detail"),
    path("chat/sessions/<uuid:session_id>/messages/", views.ChatMessageListCreateView.as_view(), name="chat-messages"),
]
