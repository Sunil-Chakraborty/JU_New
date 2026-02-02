from django.db import models
from django.conf import settings


class FeedbackSession(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedback_sessions'
    )
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = (
        ('text', 'Short Text'),
        ('textarea', 'Long Text'),
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
        ("yes_no", "Yes / No"),
        ('rating', 'Rating (1–5)'),
    )

    session = models.ForeignKey(
        FeedbackSession,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    text = models.CharField(max_length=500)
    q_type = models.CharField(max_length=20, choices=QUESTION_TYPES)

    def __str__(self):
        return self.text


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options'
    )
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text
