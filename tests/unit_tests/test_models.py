import pytest
from core.models import Task


@pytest.mark.django_db
def test_create_task():
    task = Task.objects.create(title="Test task", description="Description here")
    assert task.id is not None
    assert task.title == "Test task"
    assert task.description == "Description here"
    assert task.completed is False


@pytest.mark.django_db
def test_str_representation():
    task = Task.objects.create(title="Sample", description="...")
    assert str(task) == "Sample"


@pytest.mark.django_db
def test_completed_default_false():
    task = Task.objects.create(title="Task default")
    assert task.completed is False


@pytest.mark.django_db
def test_task_can_be_marked_complete():
    task = Task.objects.create(title="Complete me")
    task.completed = True
    task.save()
    task.refresh_from_db()
    assert task.completed is True
