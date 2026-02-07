from django import forms
from instructor.models.question_models import FeedbackSession


class FeedbackSessionForm(forms.ModelForm):
    copy_from = forms.ModelChoiceField(
        queryset=FeedbackSession.objects.none(),
        required=False,
        label="Copy questions from"
    )

    class Meta:
        model = FeedbackSession
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop("teacher", None)
        super().__init__(*args, **kwargs)

        if teacher:
            self.fields["copy_from"].queryset = (
                FeedbackSession.objects.filter(teacher=teacher)
            )
