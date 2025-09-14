from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.models import Position, Task, TaskType


class ModelsTests(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="test_position")
        self.assertEqual(str(position), position.name)

    def test_author_str(self):
        worker = get_user_model().objects.create_user(
            username="test_username",
            password="test_password_123",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEqual(
            str(worker),
            f"{worker.username} ({worker.first_name} {worker.last_name})"
        )

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="test_task_type")
        self.assertEqual(str(task_type), task_type.name)

    def test_task_str(self):
        task_type = TaskType.objects.create(name="test_task_type")
        task = Task.objects.create(
            name="test_task",
            task_type=task_type,
        )
        self.assertEqual(str(task), task.name)

    def test_create_worker_with_position(self):
        username = "test_username"
        password = "test_password_123"
        position = Position.objects.create(name="test_position")
        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=position,
        )
        self.assertEqual(worker.username, username)
        self.assertEqual(worker.position.id, position.id)
        self.assertTrue(worker.check_password(password))
