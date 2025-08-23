from django.urls import path

from task_manager.views import (
    index,
    password_change,
    TaskCompletedView,
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
    WorkerCreateView,
    WorkerDetailView,
    WorkerUpdateView,
)

urlpatterns = [
    path(
        "",
        index,
        name="index"
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "tasks/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "tasks/<int:pk>/detail/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "task/<int:pk>/task_completed/",
        TaskCompletedView.as_view(),
        name="task-completed"
    ),
    path(
        "worker/create/",
        WorkerCreateView.as_view(),
        name="worker-create"
    ),
    path(
        "worker/<int:pk>/profile/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "worker/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "change-password/",
        password_change,
        name="change-password"
    ),
]

app_name = "task_manager"
