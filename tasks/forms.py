from django import forms
from django.contrib.auth.models import User
from .models import Task

class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name="User"),
        required=True,
        label="Assign to Employee"
    )

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control"
        }),
        label="Due Date"
    )

    class Meta:
        model = Task
        fields = ["title", "description", "assigned_to", "status", "due_date"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter task title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Describe the task..."
            }),
            "status": forms.Select(attrs={
                "class": "form-select"
            }),
        }

class UserTaskForm(forms.Form):
    status = forms.ChoiceField(
        choices=Task.STATUS,
        label="Update Status",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    remark = forms.CharField(
        required=False,
        label="Add Remark (Optional)",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "placeholder": "Add an update about this task..."
        })
    )