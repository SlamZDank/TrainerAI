from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer


class ChatSessionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = ChatSession.objects.filter(user=request.user)
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request):
        session = ChatSession.objects.create(user=request.user)
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatSessionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_session(self, request, session_id):
        try:
            return ChatSession.objects.get(id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return None

    def delete(self, request, session_id):
        session = self._get_session(request, session_id)
        if session is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChatMessageListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_session(self, request, session_id):
        try:
            return ChatSession.objects.get(id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return None

    def get(self, request, session_id):
        session = self._get_session(request, session_id)
        if session is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        messages = session.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, session_id):
        session = self._get_session(request, session_id)
        if session is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChatMessageSerializer(
            data={**request.data, "session": str(session.id)}
        )
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        message = serializer.save()
        # Touch the session's updated_at
        session.save(update_fields=["updated_at"])
        return Response(ChatMessageSerializer(message).data, status=status.HTTP_201_CREATED)
