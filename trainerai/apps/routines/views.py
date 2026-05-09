from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Routine
from .serializers import RoutineSerializer

class RoutineListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        routines = Routine.objects.filter(user=request.user)
        serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoutineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoutineDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_routine(self, request, routine_id):
        try:
            return Routine.objects.get(id=routine_id, user=request.user)
        except Routine.DoesNotExist:
            return None

    def get(self, request, routine_id):
        routine = self._get_routine(request, routine_id)
        if not routine:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(RoutineSerializer(routine).data)

    def patch(self, request, routine_id):
        routine = self._get_routine(request, routine_id)
        if not routine:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RoutineSerializer(routine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, routine_id):
        routine = self._get_routine(request, routine_id)
        if not routine:
            return Response(status=status.HTTP_404_NOT_FOUND)
        routine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserRoutineListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        routines = Routine.objects.filter(user_id=user_id)
        serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data)