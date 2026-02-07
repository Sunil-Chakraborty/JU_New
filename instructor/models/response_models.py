from django.db import models
from instructor.models.question_models import FeedbackSession, Question

# Prevent duplicate feedback
class FeedbackResponse(models.Model):
    session = models.ForeignKey(
        FeedbackSession,
        on_delete=models.CASCADE,
        related_name='responses'
    )

    device_token = models.CharField(max_length=200)   # NEW FIELD

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("session", "device_token")  # 🚫 one submission per device


class Answer(models.Model):
    response = models.ForeignKey(
        FeedbackResponse,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    answer_text = models.TextField(blank=True)
