from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.models import Position


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test_admin_password_123",
        )
        self.client.force_login(self.admin_user)
        self.worker_position = Position.objects.create(name="test_position")
        self.worker = get_user_model().objects.create_user(
            username="test_worker",
            password="test_worker_password_123",
            position=self.worker_position,
        )

    def test_position_model_is_registered(self):
        """
        Test that admin can manage Positions on admin page
        :return:
        """
        url = reverse("admin:index")
        res = self.client.get(url)
        self.assertContains(res, "Positions")

    def test_task_type_model_is_registered(self):
        """
        Test that admin can manage TaskTypes on admin page
        :return:
        """
        url = reverse("admin:index")
        res = self.client.get(url)
        self.assertContains(res, "Task types")

    def test_task_model_is_registered(self):
        """
        Test that admin can manage Tasks on admin page
        :return:
        """
        url = reverse("admin:index")
        res = self.client.get(url)
        self.assertContains(res, "Tasks")

    def test_worker_model_is_registered(self):
        """
        Test that admin can manage Workers on admin page
        :return:
        """
        url = reverse("admin:index")
        res = self.client.get(url)
        self.assertContains(res, "Workers")

    def test_worker_position_listed(self):
        """
        Test that worker's position is in list_display on author admin page
        :return: None
        """
        url = reverse("admin:task_manager_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker_position.name)

    def test_worker_detail_position_listed(self):
        """
        Test that worker's position is on author detail admin page
        :return: None
        """
        url = reverse(
            "admin:task_manager_worker_change",
            args=[self.worker.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.worker_position.name)

    def test_worker_add_additional_fields_listed(self):
        """
        Test that there are additional first_name, last_name
        and position fields on worker creation admin page
        :return:
        """
        url = reverse("admin:task_manager_worker_add")
        res = self.client.get(url)
        self.assertContains(res, "first_name")
        self.assertContains(res, "last_name")
        self.assertContains(res, "position")
