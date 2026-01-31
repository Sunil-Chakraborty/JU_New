# instructor/forms/registration.py
from django import forms
from instructor.models import CustomUser
from instructor.utils.validators import validate_email_domain

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "user_type"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if not validate_email_domain(email):
            raise forms.ValidationError("Use official @jdvu.com email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email

    def clean_user_type(self):
        user_type = self.cleaned_data["user_type"]
        if user_type == "admin":
            raise forms.ValidationError("Admin cannot register here")
        return user_type


