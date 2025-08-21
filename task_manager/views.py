from django.shortcuts import render
from django.views import generic

from task_manager.models import Task


# Create your views here.


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.all().select_related("task_type").prefetch_related("assignees")
    template_name = "task_manager/index.html"
    context_object_name = "task_list"
