from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Task, TaskType

TASK_LIST_URL = reverse("task_manager:task-list")


class PublicTaskTest(TestCase):
    def test_task_list_login_required(self):
        res = self.client.get(TASK_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_task_detail_login_required(self):
        task_type = TaskType.objects.create(name="test_task_type")
        task = Task.objects.create(
            name="test_task",
            task_type=task_type,
        )
        url = reverse("task_manager:task-detail", args=[task.id])
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password_123",
        )
        self.client.force_login(self.user)
        self.task_type1 = TaskType.objects.create(name="test_task_type1")
        self.task_type2 = TaskType.objects.create(name="test_task_type2")
        self.task1 = Task.objects.create(
            name="test_task1", task_type=self.task_type1
        )
        self.task2 = Task.objects.create(
            name="test_task2", task_type=self.task_type2
        )

        self.create_url = reverse("task_manager:task-create")
        self.test_task_data = {
            "name": "new_task",
            "description": "some_test_description",
            "priority": "Normal",
            "task_type": self.task_type1.id,
        }

    def test_retrieve_task_list(self):
        response = self.client.get(TASK_LIST_URL)
        self.assertEqual(response.status_code, 200)

        received_tasks = response.context["task_list"]
        self.assertEqual(len(received_tasks), 2)
        self.assertIn(self.task1, received_tasks)
        self.assertIn(self.task2, received_tasks)

        existing_tasks = Task.objects.all()
        self.assertListEqual(list(received_tasks), list(existing_tasks))

        task3 = Task.objects.create(
            name="test_task3", task_type=self.task_type1
        )
        self.assertNotIn(task3, received_tasks)

        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_task_create_view(self):
        response = self.client.post(self.create_url, self.test_task_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="new_task").exists())

    def test_task_create_view_fails_without_name_field(self):
        data = self.test_task_data
        data.pop("name")
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(name="new_task").exists())
        self.assertContains(response, "This field is required.")

    def test_task_create_view_fails_without_description_field(self):
        data = self.test_task_data
        data.pop("description")
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(name="new_task").exists())
        self.assertContains(response, "This field is required.")

    def test_task_create_view_fails_without_priority_field(self):
        data = self.test_task_data
        data.pop("priority")
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(name="new_task").exists())
        self.assertContains(response, "This field is required.")

    def test_task_create_view_fails_without_task_type_field(self):
        data = self.test_task_data
        data.pop("task_type")
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(name="new_task").exists())
        self.assertContains(response, "This field is required.")

    def test_task_update_view(self):
        url = reverse("task_manager:task-update", args=[self.task1.id])
        data = {
            "description": "new_updated_description",
            "is_completed": True,
            "priority": "Urgent",
        }
        response = self.client.post(url, data)
        self.assertRedirects(
            response,
            reverse(
                "task_manager:task-detail",
                args=[self.task1.id]
            )
        )
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.description, "new_updated_description")
        self.assertEqual(self.task1.is_completed, True)
        self.assertEqual(self.task1.priority, "Urgent")

    def test_task_delete_view(self):
        url = reverse("task_manager:task-delete", args=[self.task1.id])
        response = self.client.post(url)
        self.assertRedirects(response, TASK_LIST_URL)
        self.assertFalse(
            Task.objects.filter(id=self.task1.id).exists()
        )

    def test_task_completed_view(self):
        url = reverse("task_manager:task-completed", args=[self.task1.id])
        self.client.post(url)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_completed)

    def test_task_add_or_del_worker_view_add_and_remove(self):
        url = reverse(
            "task_manager:task-add-or-del-worker", args=[self.task1.id]
        )

        self.client.post(url)
        self.assertIn(self.user, self.task1.assignees.all())

        self.client.post(url)
        self.assertNotIn(self.user, self.task1.assignees.all())
