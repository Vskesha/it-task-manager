from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

WORKER_LIST_URL = reverse("task_manager:worker-list")

User = get_user_model()


class WorkerViewTests(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin",
            password="adminPass",
        )
        self.user = User.objects.create_user(
            username="simple_user",
            password="userPass",
        )

    def test_worker_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(WORKER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/worker_list.html")

    def test_worker_create_requires_superuser(self):
        url = reverse("task_manager:worker-create")

        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_worker_delete_requires_superuser(self):
        worker = User.objects.create_user(
            username="temporary",
            password="tempPass123",
        )
        url = reverse("task_manager:worker-delete", args=[worker.id])

        self.client.force_login(self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.superuser)
        response = self.client.post(url)
        self.assertRedirects(response, WORKER_LIST_URL)
        self.assertFalse(User.objects.filter(username="temporary").exists())
