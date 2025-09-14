from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Task, TaskType

INDEX_URL = reverse("task_manager:index")

User = get_user_model()


class IndexViewTests(TestCase):
    def test_index_view_context(self):
        user = User.objects.create_user(
            username="simple_user",
            password="userPass",
        )
        self.task_type1 = TaskType.objects.create(name="test_task_type1")
        self.task1 = Task.objects.create(
            name="test_task1", task_type=self.task_type1
        )
        self.client.force_login(user)
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)


class PasswordChangeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="simple_user",
            password="userPass",
        )
        self.client.force_login(self.user)

    def test_password_change_success(self):
        url = reverse("task_manager:change-password")
        data = {
            "new_password1": "newPass123",
            "new_password2": "newPass123"
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("login"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newPass123"))

    def test_password_change_failure(self):
        url = reverse("task_manager:change-password")
        data = {
            "new_password1": "newPass123",
            "new_password2": "differentPass"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields didn’t match")
