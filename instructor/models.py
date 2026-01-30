# instructor/models.py

from django.db import models

class InstructorEmailVerification(models.Model):
    instructor = models.OneToOneField(
        "Instructor",
        on_delete=models.CASCADE
    )
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.instructor.email
