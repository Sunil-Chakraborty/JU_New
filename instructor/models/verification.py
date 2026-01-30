from django.db import models
from django.conf import settings
import uuid

class InstructorEmailVerification(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - verified={self.is_verified}"
