from django import forms
from instructor.models.teacher import Teacher
from instructor.models.accounts import Department
from django.db.models import Min

class TeacherForm(forms.ModelForm):

    # 1. Get the minimum ID for each unique department name
    unique_ids = (
        Department.objects
        .values("name")
        .annotate(min_id=Min("id"))
        .values_list("min_id", flat=True)
    )

    # 2. Filter departments using those IDs
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(id__in=unique_ids).order_by("name"),
        empty_label="Select Department",
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    class Meta:
        model = Teacher
        exclude = ("user", "created_date", "updated_date")
       
                
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "doj": forms.DateInput(attrs={"type": "date"}),
        }
