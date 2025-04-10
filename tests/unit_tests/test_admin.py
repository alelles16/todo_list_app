import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import Task


User = get_user_model()


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        email="admin@example.com", username="admin", password="adminpass"
    )


@pytest.fixture
def authenticated_admin_client(admin_user, client):
    client.force_login(admin_user)
    return client


@pytest.mark.django_db
def test_admin_login_page_loads(client):
    response = client.get(reverse("admin:login"))
    assert response.status_code == 200
    assert b"Log in" in response.content


@pytest.mark.django_db
def test_admin_login_success(authenticated_admin_client):
    response = authenticated_admin_client.get(reverse("admin:index"))
    assert response.status_code == 200
    assert b"Site administration" in response.content


@pytest.mark.django_db
def test_task_model_visible_in_admin(authenticated_admin_client):
    url = reverse("admin:core_task_changelist")
    response = authenticated_admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_task_model_editable_in_admin(authenticated_admin_client):
    task = Task.objects.create(title="Admin Task", description="From admin")
    url = reverse("admin:core_task_change", args=[task.id])
    response = authenticated_admin_client.get(url)
    assert response.status_code == 200
    assert b"Change task" in response.content
    assert b"Admin Task" in response.content


@pytest.mark.django_db
def test_task_model_add_view(authenticated_admin_client):
    url = reverse("admin:core_task_add")
    response = authenticated_admin_client.get(url)
    assert response.status_code == 200
    assert b"Add task" in response.content
