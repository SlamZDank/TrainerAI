import uuid
from django.db import models
from trainerai.apps.authentication.models import User

class Routine(models.Model):
    class DayName(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
        SUNDAY = 'sunday', 'Sunday'

    class Status(models.TextChoices):
        DONE = 'done', 'Done'
        NOT_DONE = 'not_done', 'Not Done'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="routines")
    activity_name = models.CharField(max_length=200)
    activity_description = models.TextField(blank=True, default='')
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_name = models.CharField(max_length=10, choices=DayName.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.NOT_DONE)

    class Meta:
        app_label = 'routines'
        ordering = ["day_name", "start_time"]
