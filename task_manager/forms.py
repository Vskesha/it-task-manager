from django import forms

from task_manager.models import Task


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["description", "is_completed"]


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search of name task",
                "style": "width: 400px;"
            }
        )
    )
