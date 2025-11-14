from django import forms
from django.contrib.auth.models import User
from .models import Task, TaskRemark

class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name="User"),
        required=True,
        label="Assign to User"
    )

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Due Date"
    )

    class Meta:
        model = Task
        fields = ["title", "description", "assigned_to", "status", "due_date"]

class UserTaskForm(forms.Form):
    status = forms.ChoiceField(choices=Task.STATUS, label="Status")
    remark = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False, label="Add remark (optional)")
