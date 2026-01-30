from django import forms
from instructor.models.teacher import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ("user", "created_date", "updated_date")
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "doj": forms.DateInput(attrs={"type": "date"}),
        }
