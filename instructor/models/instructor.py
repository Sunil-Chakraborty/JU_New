from django.db import models
from django.conf import settings
from django.utils import timezone
import os

class Instructor(models.Model):
    user = models.OneToOneField(
        "instructor.CustomUser",
        on_delete=models.CASCADE,
        related_name="instructor_profile",
    )

    department = models.ForeignKey(
        "instructor.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="instructors",
    )
    name            = models.CharField(max_length=100)
    email           = models.EmailField(unique=True)
    short_intro     = models.CharField(max_length=200, blank=True, null=True)
    bio             = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
