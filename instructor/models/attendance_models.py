# Tracks virtual headcount (NOT identity)

from django.db import models
from instructor.models.question_models import FeedbackSession


class SessionAttendance(models.Model):
    session = models.ForeignKey(
        FeedbackSession,
        on_delete=models.CASCADE,
        related_name="attendances"
    )
    device_token = models.CharField(max_length=200)


    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("session", "device_token")  # prevent duplicate presence
