from django.urls import reverse_lazy
from django.views import generic

from task_manager.models import Task


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.all().select_related("task_type").prefetch_related("assignees__tasks")
    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"


class TaskCreateView(generic.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDetailView(generic.DetailView):
    model = Task


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = ["description", "is_completed"]
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")
