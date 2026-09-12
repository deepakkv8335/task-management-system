from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from .models import Task, TaskRemark
from .forms import TaskForm, UserTaskForm

def is_manager(user):
    return user.groups.filter(name="Manager").exists()

def is_user(user):
    return user.groups.filter(name="User").exists()

@login_required
def dashboard(request):

    if request.user.is_superuser:
        return render(request, "tasks/dashboard_admin.html")

    if is_manager(request.user):
        tasks = Task.objects.all()
        return render(request, "tasks/dashboard_manager.html", {
            "tasks": tasks
        })

    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, "tasks/dashboard_user.html", {
        "tasks": tasks
    })

@login_required
def create_task(request):
    if not (request.user.is_superuser or is_manager(request.user)):
        return redirect("dashboard")

    form = TaskForm(request.POST or None)

    if form.is_valid():
        task = form.save(commit=False)
        task.created_by = request.user
        task.save()
        return redirect("dashboard")

    return render(request, "tasks/task_edit.html", {"form": form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if is_user(request.user) and task.assigned_to != request.user:
        return HttpResponseForbidden("You do not have permission to edit this task.")

    if is_user(request.user) and not request.user.is_superuser:
        form = UserTaskForm(request.POST or None, initial={'status': task.status})
        if request.method == "POST" and form.is_valid():
            task.status = form.cleaned_data['status']
            task.save()
            remark_text = form.cleaned_data.get('remark', '').strip()
            if remark_text:
                TaskRemark.objects.create(task=task, user=request.user, text=remark_text)
            return redirect('task_detail', task_id=task.id)
        return render(request, "tasks/task_user_update.html", {"form": form, "task": task})

    if not (request.user.is_superuser or is_manager(request.user)):
        return HttpResponseForbidden("You do not have permission to edit this task.")

    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('task_detail', task_id=task.id)

    return render(request, "tasks/task_edit.html", {"form": form, "task": task})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    remarks = task.remarks.select_related('user').all()

    return render(request, "tasks/task_detail.html", {"task": task, "remarks": remarks})
