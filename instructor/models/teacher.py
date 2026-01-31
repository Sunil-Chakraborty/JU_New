from django.db import models
from django.conf import settings
from django.utils import timezone
import os
from instructor.models.accounts import Department


# -----------------------------
# Utility: Image Upload Path
# -----------------------------
def get_image_path(instance, filename):
    return os.path.join("general", f"user_{instance.user_id}", filename)


# -----------------------------
# Teacher Profile
# -----------------------------
class Teacher(models.Model):
    user = models.OneToOneField(
        "instructor.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teacher_profile",
    )

    first_name = models.CharField(max_length=100, blank=True, null=True)
    dept_name = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    group_name = models.CharField(max_length=100, blank=True, null=True)

    dob = models.DateField(null=True, blank=True)

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)

    CAST_CHOICES = (
        ("SC", "SC"),
        ("ST", "ST"),
        ("OBC-A", "OBC-A"),
        ("OBC-B", "OBC-B"),
        ("GEN", "GEN"),
    )
    caste = models.CharField(max_length=10, choices=CAST_CHOICES, null=True, blank=True)

    DESIGNATION_CHOICES = (
        ("AP", "Assistant Professor"),
        ("ASP", "Associate Professor"),
    )
    designation = models.CharField(
        max_length=30, choices=DESIGNATION_CHOICES, null=True, blank=True
    )

    doj = models.DateField(null=True, blank=True)
    exp = models.PositiveIntegerField(default=0)

    mobile = models.CharField(max_length=10, null=True, blank=True)

    photo = models.ImageField(upload_to=get_image_path, null=True, blank=True)

    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if self.department:
            self.dept_name = self.department.name
        else:
            self.dept_name = ""
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email if self.user else "Teacher Profile"
