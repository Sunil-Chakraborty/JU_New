from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils import timezone
import os

# https://chatgpt.com/c/697f862b-22c8-8322-94c1-849c928d164a

# ✅ FIXED MANAGER (EMAIL-BASED)
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # ✅ for OTP-first users

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# ✅ FIXED USER MODEL
class CustomUser(AbstractBaseUser, PermissionsMixin):

    USER_TYPES = (
        ("teacher", "Teacher"),
        ("instructor", "Instructor"),
    )

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    objects = CustomUserManager()   # ✅ CRITICAL LINE

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_type"]

    def __str__(self):
        return self.email


# (unchanged)
class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100, blank=True, null=True)
    program = models.CharField(max_length=200, blank=True, null=True)
    prog_cd = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
 