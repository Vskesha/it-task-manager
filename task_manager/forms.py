from django import forms

from task_manager.models import Task


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["description", "is_completed"]
