from django import forms
from instructor.models.question_models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "q_type"]
        widgets = {
            "text": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter question text",
                }
            ),
            "q_type": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "questionType",
                }
            ),
        }
