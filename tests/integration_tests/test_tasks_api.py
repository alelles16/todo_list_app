import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Task


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_task():
    return Task.objects.create(title="Test Task", description="This is a test task")


@pytest.mark.django_db
def test_list_tasks(api_client, sample_task):
    url = reverse("task-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["title"] == sample_task.title


@pytest.mark.django_db
def test_list_multiple_tasks_ordered(api_client):
    tasks = [
        Task.objects.create(title="Third Task", description="Yet another test task"),
        Task.objects.create(title="Another Task", description="Another test task"),
        Task.objects.create(title="Test Task", description="This is a test task"),
    ]
    url = reverse("task-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(tasks)

    returned_titles = [task["title"] for task in response.data]
    expected_titles = [task.title for task in Task.objects.order_by("-id")]
    assert returned_titles == expected_titles


@pytest.mark.django_db
def test_create_task(api_client):
    url = reverse("task-list")
    payload = {"title": "New Task", "description": "Create task test"}
    response = api_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.filter(title="New Task").exists()


@pytest.mark.django_db
def test_create_task_missing_title(api_client):
    url = reverse("task-list")
    payload = {"description": "Missing title"}
    response = api_client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "title" in response.data


@pytest.mark.django_db
def test_get_single_task(api_client, sample_task):
    url = reverse("task-detail", args=[sample_task.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == sample_task.title


@pytest.mark.django_db
def test_get_nonexistent_task_returns_404(api_client):
    url = reverse("task-detail", args=[999])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "Tasks not found."


@pytest.mark.django_db
def test_update_task(api_client, sample_task):
    url = reverse("task-detail", args=[sample_task.id])
    updated_data = {"title": "Updated Task", "description": "Updated"}
    response = api_client.put(url, updated_data)
    assert response.status_code == status.HTTP_200_OK
    sample_task.refresh_from_db()
    assert sample_task.title == "Updated Task"


@pytest.mark.django_db
def test_partial_update_task(api_client, sample_task):
    url = reverse("task-detail", args=[sample_task.id])
    response = api_client.patch(url, {"title": "Patched Title"})
    assert response.status_code == status.HTTP_200_OK
    sample_task.refresh_from_db()
    assert sample_task.title == "Patched Title"


@pytest.mark.django_db
def test_delete_task(api_client, sample_task):
    url = reverse("task-detail", args=[sample_task.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Task.objects.filter(id=sample_task.id).exists()
