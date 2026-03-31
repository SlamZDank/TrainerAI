from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatSession, ChatMessage, WorkoutPlan, DietPlan
from .serializers import ChatSessionSerializer, ChatMessageSerializer, WorkoutPlanSerializer, DietPlanSerializer


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

    def patch(self, request, session_id):
        session = self._get_session(request, session_id)
        if session is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ChatSessionSerializer(session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class WorkoutPlanListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = WorkoutPlan.objects.filter(user=request.user)
        return Response(WorkoutPlanSerializer(plans, many=True).data)

    def post(self, request):
        session = None
        session_id = request.data.get("session_id")
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id, user=request.user)
            except ChatSession.DoesNotExist:
                pass
        plan = WorkoutPlan.objects.create(
            user=request.user,
            session=session,
            title=request.data.get("title", ""),
            content=request.data.get("content", ""),
        )
        return Response(WorkoutPlanSerializer(plan).data, status=status.HTTP_201_CREATED)


class DietPlanListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = DietPlan.objects.filter(user=request.user)
        return Response(DietPlanSerializer(plans, many=True).data)

    def post(self, request):
        session = None
        session_id = request.data.get("session_id")
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id, user=request.user)
            except ChatSession.DoesNotExist:
                pass
        plan = DietPlan.objects.create(
            user=request.user,
            session=session,
            title=request.data.get("title", ""),
            content=request.data.get("content", ""),
        )
        return Response(DietPlanSerializer(plan).data, status=status.HTTP_201_CREATED)


class WorkoutPlanDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_plan(self, request, plan_id):
        try:
            return WorkoutPlan.objects.get(id=plan_id, user=request.user)
        except WorkoutPlan.DoesNotExist:
            return None

    def get(self, request, plan_id):
        plan = self._get_plan(request, plan_id)
        if not plan:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(WorkoutPlanSerializer(plan).data)

    def patch(self, request, plan_id):
        plan = self._get_plan(request, plan_id)
        if not plan:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WorkoutPlanSerializer(plan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, plan_id):
        plan = self._get_plan(request, plan_id)
        if not plan:
            return Response(status=status.HTTP_404_NOT_FOUND)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DietPlanDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_plan(self, request, plan_id):
        try:
            return DietPlan.objects.get(id=plan_id, user=request.user)
        except DietPlan.DoesNotExist:
            return None

    def get(self, request, plan_id):
        plan = self._get_plan(request, plan_id)
        if not plan:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(DietPlanSerializer(plan).data)

    def patch(self, request, plan_id):
        plan = self._get_plan(request, plan_id)
        if not plan:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DietPlanSerializer(plan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, plan_id):
        plan = self._get_plan(request, plan_id)
        if not plan:
            return Response(status=status.HTTP_404_NOT_FOUND)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
