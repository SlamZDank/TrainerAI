from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Routine
from .serializers import RoutineSerializer

def lazy_reset_routines(user):
    today = timezone.now().date()
    # In Python, Monday is 0 and Sunday is 6.
    # To find the most recent Sunday:
    # If today is Sunday (6), last_sunday is today.
    # If today is Monday (0), last_sunday is 1 day ago.
    days_since_sunday = (today.weekday() + 1) % 7
    last_sunday = today - timedelta(days=days_since_sunday)
    
    # Routines last updated before the most recent Sunday should be reset if they are done
    routines_to_reset = Routine.objects.filter(
        user=user, 
        last_status_update__lt=last_sunday,
        status=Routine.Status.DONE
    )
    
    if routines_to_reset.exists():
        routines_to_reset.update(status=Routine.Status.NOT_DONE, last_status_update=today)
    
    # Update last_status_update for NOT_DONE routines too, so we don't keep checking them unnecessarily
    Routine.objects.filter(
        user=user,
        last_status_update__lt=last_sunday,
        status=Routine.Status.NOT_DONE
    ).update(last_status_update=today)


class RoutineListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lazy_reset_routines(request.user)
        routines = Routine.objects.filter(user=request.user)
        serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoutineSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, last_status_update=timezone.now().date())
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
        
        # If status is being updated, update last_status_update
        data = request.data.copy()
        if 'status' in data:
            data['last_status_update'] = timezone.now().date()

        serializer = RoutineSerializer(routine, data=data, partial=True, context={'request': request})
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
        # We probably shouldn't trigger another user's lazy reset here unless requested, 
        # but doing it ensures accurate data. Let's do it if we can get the user.
        from trainerai.apps.authentication.models import User
        try:
            target_user = User.objects.get(id=user_id)
            lazy_reset_routines(target_user)
        except User.DoesNotExist:
            pass

        routines = Routine.objects.filter(user_id=user_id)
        serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data)