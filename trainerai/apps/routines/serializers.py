from rest_framework import serializers
from .models import Routine

class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ["id", "activity_name", "activity_description", "start_time", "end_time", "day_name", "status", "last_status_update"]
        read_only_fields = ["id", "last_status_update"]

    def validate(self, data):
        # Handle partial updates (PATCH)
        start_time = data.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = data.get('end_time', getattr(self.instance, 'end_time', None))
        day_name = data.get('day_name', getattr(self.instance, 'day_name', None))
        
        # In a POST request, 'user' isn't in 'data' yet because it's assigned in the view's perform_create or save()
        # We get it from the context
        user = self.context['request'].user

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")

        # Check for overlaps
        if all([start_time, end_time, day_name]):
            queryset = Routine.objects.filter(user=user, day_name=day_name)
            
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            # Overlap logic: (StartA < EndB) and (EndA > StartB)
            conflicts = queryset.filter(
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()

            if conflicts:
                raise serializers.ValidationError({
                    "non_field_errors": ["This routine conflicts with an existing one on the same day."],
                    "code": "overlap_conflict"
                })

        return data
