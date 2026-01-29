import uuid
from django.db import models


class FeedbackSession(models.Model):
    title = models.CharField(max_length=200)

    instructor = models.ForeignKey(
        "instructor.Instructor",
        on_delete=models.CASCADE,
        related_name="feedback_sessions",
    )

    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
