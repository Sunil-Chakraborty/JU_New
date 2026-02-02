from django.db import models
from instructor.models.question_models import FeedbackSession, Question


class FeedbackResponse(models.Model):
    session = models.ForeignKey(
        FeedbackSession,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)


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
