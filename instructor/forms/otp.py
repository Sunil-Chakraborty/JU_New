from django import forms

class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        label="OTP Code"
    )
