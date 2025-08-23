from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["username"]

    def __str__(self) -> str:
        return (f"{self.username} (Full name: "
               f"{self.first_name} {self.last_name} "
               f"Position: {self.position})")

    def get_absolute_url(self) -> str:
        return reverse("cabinet:worker-detail", kwargs={"pk": self.pk})


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Normal", "Normal"),
        ("Low", "Low")
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="Normal"
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    class Meta:
        ordering = ["-deadline"]

    def __str__(self) -> str:
        return self.name
