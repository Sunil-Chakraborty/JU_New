# instructor/models/otp.py
# One user → many OTPs
# OTP expires in 10 minutes

import random
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class EmailOTP(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # ✅ FIX
        on_delete=models.CASCADE,
        related_name="email_otps",
    )

    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    @staticmethod
    def generate_otp():
        return f"{random.randint(100000, 999999)}"
