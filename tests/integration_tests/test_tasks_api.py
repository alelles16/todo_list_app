import pytest
from rest_framework.test import APIClient
from core.models import Task


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_task():
    return Task.objects.create(title="Test Task", description="This is a test task")


@pytest.mark.django_db
def test_list_tasks(api_client, sample_task):
    response = api_client.get("/tasks/")
    assert response.status_code == 200
    assert any(task["title"] == "Test Task" for task in response.data)


@pytest.mark.django_db
def test_create_task(api_client):
    payload = {"title": "New Task", "description": "Create task test"}
    response = api_client.post("/tasks/", payload)
    assert response.status_code == 201
    assert Task.objects.filter(title="New Task").exists()


@pytest.mark.django_db
def test_get_single_task(api_client, sample_task):
    response = api_client.get(f"/tasks/{sample_task.id}/")
    assert response.status_code == 200
    assert response.data["title"] == sample_task.title


@pytest.mark.django_db
def test_get_nonexistent_task_returns_404(api_client):
    response = api_client.get("/tasks/999/")
    assert response.status_code == 404
    assert response.data["detail"] == "Tasks not found."


@pytest.mark.django_db
def test_update_task(api_client, sample_task):
    updated_data = {"title": "Updated Task", "description": "Updated"}
    response = api_client.put(f"/tasks/{sample_task.id}/", updated_data)
    assert response.status_code == 200
    sample_task.refresh_from_db()
    assert sample_task.title == "Updated Task"


@pytest.mark.django_db
def test_delete_task(api_client, sample_task):
    response = api_client.delete(f"/tasks/{sample_task.id}/")
    assert response.status_code == 204
    assert not Task.objects.filter(id=sample_task.id).exists()
