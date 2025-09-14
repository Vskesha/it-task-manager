from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.utils import timezone

from task_manager.forms import (
    ChangePasswordForm,
    TaskCreateForm,
    TaskSearchForm,
    TaskUpdateForm,
    WorkerCreateForm,
    WorkerSearchForm,
)
from task_manager.models import Position, Task, TaskType

User = get_user_model()


class TaskCreateFormTests(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="test_type")

    def test_task_create_form_valid_data(self):
        future_date = timezone.now() + timedelta(days=1)
        form_data = {
            "name": "Test Task",
            "description": "Test task description",
            "deadline": future_date,
            "is_completed": False,
            "priority": "Urgent",
            "assignees": [self.user.id],
            "task_type": self.task_type,
        }
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_create_form_past_deadline_invalid(self):
        past_date = timezone.now() - timedelta(days=1)
        form_data = {
            "name": "Test Task",
            "description": "Test task description",
            "deadline": past_date,
            "is_completed": False,
            "priority": "medium",
        }
        form = TaskCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)
        self.assertEqual(
            form.errors["deadline"][0],
            "The date is incorrect. Date < today's date"
        )

    def test_task_create_form_no_deadline_valid(self):
        form_data = {
            "name": "Test Task",
            "description": "Test task description",
            "is_completed": False,
            "priority": "Low",
            "task_type": self.task_type,
        }
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_create_form_assignees_not_required(self):
        form_data = {
            "name": "Test Task",
            "description": "Test task description",
            "is_completed": False,
            "priority": "Urgent",
            "task_type": self.task_type,
        }
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_create_form_multiple_assignees(self):
        user2 = User.objects.create_user(
            username="testuser2",
            password="testpass123",
            position=self.position
        )
        form_data = {
            "name": "Test Task",
            "description": "Test task description",
            "is_completed": False,
            "priority": "Normal",
            "assignees": [self.user.id, user2.id],
            "task_type": self.task_type,
        }
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())


class TaskUpdateFormTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.position = Position.objects.create(name="Developer")
        self.regular_user = User.objects.create_user(
            username="regular",
            password="testpass123",
            position=self.position
        )
        self.superuser = User.objects.create_superuser(
            username="admin",
            password="testpass123",
            email="admin@test.com"
        )
        self.task_type = TaskType.objects.create(
            name="test_type"
        )
        self.task = Task.objects.create(
            name="Test Task",
            description="Test description",
            priority="medium",
            task_type=self.task_type
        )

    def test_task_update_form_superuser_has_all_fields(self):
        request = self.factory.get("/")
        request.user = self.superuser
        form = TaskUpdateForm(request=request, instance=self.task)

        expected_fields = [
            "description", "is_completed", "priority", "deadline", "assignees"
        ]
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_task_update_form_regular_user_limited_fields(self):
        request = self.factory.get("/")
        request.user = self.regular_user
        form = TaskUpdateForm(request=request, instance=self.task)

        expected_fields = ["description", "is_completed", "priority"]
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_task_update_form_valid_data_regular_user(self):
        request = self.factory.get("/")
        request.user = self.regular_user
        form_data = {
            "description": "Updated description",
            "is_completed": True,
            "priority": "Normal",
        }
        form = TaskUpdateForm(
            data=form_data,
            request=request,
            instance=self.task
        )
        self.assertTrue(form.is_valid())

    def test_task_update_form_valid_data_superuser(self):
        request = self.factory.get("/")
        request.user = self.superuser
        future_date = timezone.now() + timedelta(days=1)
        form_data = {
            "description": "Updated description",
            "is_completed": True,
            "priority": "Low",
            "deadline": future_date,
            "assignees": [self.regular_user.id],
        }
        form = TaskUpdateForm(
            data=form_data,
            request=request,
            instance=self.task
        )
        self.assertTrue(form.is_valid())


class TaskSearchFormTests(TestCase):

    def test_task_search_form_valid_with_name(self):
        form_data = {"name": "test task"}
        form = TaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test task")

    def test_task_search_form_valid_empty(self):
        form_data = {"name": ""}
        form = TaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_task_search_form_name_not_required(self):
        form = TaskSearchForm(data={})
        self.assertTrue(form.is_valid())


class WorkerCreateFormTests(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="test_position")

    def test_worker_creation_form_with_position_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "userPass123",
            "password2": "userPass123",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "position": self.position,
        }
        form = WorkerCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_worker_creation_form_password_mismatch(self):
        form_data = {
            "username": "new_user",
            "password1": "userPass123",
            "password2": "differentPass123",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "position": self.position.id,
        }
        form = WorkerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_worker_creation_form_weak_password(self):
        form_data = {
            "username": "new_user",
            "password1": "123",
            "password2": "123",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "position": self.position.id,
        }
        form = WorkerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_worker_creation_form_duplicate_username(self):
        # Create existing user
        User.objects.create_user(
            username="existing_user",
            password="testpass123",
            position=self.position
        )

        form_data = {
            "username": "existing_user",
            "password1": "userPass123",
            "password2": "userPass123",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "position": self.position.id,
        }
        form = WorkerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_worker_creation_form_without_names_valid(self):
        form_data = {
            "username": "new_user_no_names",
            "password1": "userPass123",
            "password2": "userPass123",
            "position": self.position.id,
        }
        form = WorkerCreateForm(data=form_data)
        self.assertTrue(form.is_valid())


class WorkerSearchFormTests(TestCase):

    def test_worker_search_form_valid_with_username(self):
        form_data = {"username": "testuser"}
        form = WorkerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")

    def test_worker_search_form_valid_empty(self):
        form_data = {"username": ""}
        form = WorkerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_worker_search_form_username_not_required(self):
        form = WorkerSearchForm(data={})
        self.assertTrue(form.is_valid())


class ChangePasswordFormTests(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = User.objects.create_user(
            username="testuser",
            password="oldpass123",
            position=self.position
        )

    def test_change_password_form_valid_data(self):
        form_data = {
            "new_password1": "newStrongPass123",
            "new_password2": "newStrongPass123",
        }
        form = ChangePasswordForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_change_password_form_password_mismatch(self):
        form_data = {
            "new_password1": "newStrongPass123",
            "new_password2": "differentPass123",
        }
        form = ChangePasswordForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("new_password2", form.errors)

    def test_change_password_form_weak_password(self):
        form_data = {
            "new_password1": "123",
            "new_password2": "123",
        }
        form = ChangePasswordForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("new_password2", form.errors)

    def test_change_password_form_empty_passwords(self):
        form_data = {
            "new_password1": "",
            "new_password2": "",
        }
        form = ChangePasswordForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("new_password1", form.errors)
