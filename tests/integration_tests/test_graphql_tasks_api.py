import pytest
from todolist.graphql.schema import schema
from core.models import Task


@pytest.mark.django_db
def test_create_task():
    response = schema.execute_sync(
        """
        mutation CreateTask($data: TaskInput!) {
            createTask(data: $data) {
                id
                title
                description
                completed
            }
        }
        """,
        variable_values={
            "data": {"title": "Test Task", "description": "Testing", "completed": False}
        },
    )
    task_data = response.data["createTask"]
    assert task_data["title"] == "Test Task"
    assert Task.objects.filter(id=task_data["id"]).exists()


@pytest.mark.django_db
def test_list_tasks():
    Task.objects.create(title="T1", description="...", completed=False)
    Task.objects.create(title="T2", description="...", completed=True)

    response = schema.execute_sync(
        """
        query {
            tasks {
                id
                title
                completed
            }
        }
        """
    )

    assert len(response.data["tasks"]) == 2
    assert any(t["title"] == "T2" for t in response.data["tasks"])


@pytest.mark.django_db
def test_get_task_by_id():
    task = Task.objects.create(
        title="Unique Task", description="Detail", completed=False
    )

    response = schema.execute_sync(
        """
        query GetTask($id: Int!) {
            task(id: $id) {
                id
                title
            }
        }
        """,
        variable_values={"id": task.id},
    )

    assert response.data["task"]["title"] == "Unique Task"


@pytest.mark.django_db
def test_update_task():
    task = Task.objects.create(title="To Update", description="...", completed=False)

    response = schema.execute_sync(
        """
        mutation UpdateTask($taskId: Int!, $data: TaskUpdateInput!) {
            updateTask(taskId: $taskId, data: $data) {
                id
                title
                completed
            }
        }
        """,
        variable_values={
            "taskId": task.id,
            "data": {"title": "Updated!", "completed": True},
        },
    )

    task.refresh_from_db()
    assert response.data["updateTask"]["title"] == "Updated!"
    assert task.completed is True


@pytest.mark.django_db
def test_delete_task():
    task = Task.objects.create(title="To Delete")

    response = schema.execute_sync(
        """
        mutation DeleteTask($taskId: Int!) {
            deleteTask(taskId: $taskId)
        }
        """,
        variable_values={"taskId": task.id},
    )

    assert response.data["deleteTask"] is True
    assert not Task.objects.filter(pk=task.id).exists()


@pytest.mark.django_db
def test_get_nonexistent_task():
    response = schema.execute_sync(
        """
        query GetTask($id: Int!) {
            task(id: $id) {
                id
                title
            }
        }
        """,
        variable_values={"id": 9999},
    )
    assert response.errors
    assert "not found" in str(response.errors[0])


@pytest.mark.django_db
def test_update_task_with_no_changes():
    task = Task.objects.create(title="Initial", description="...", completed=False)

    response = schema.execute_sync(
        """
        mutation UpdateTask($taskId: Int!, $data: TaskUpdateInput!) {
            updateTask(taskId: $taskId, data: $data) {
                id
                title
                description
                completed
            }
        }
        """,
        variable_values={"taskId": task.id, "data": {}},
    )

    task.refresh_from_db()
    assert response.data["updateTask"]["title"] == "Initial"
    assert task.completed is False


@pytest.mark.django_db
def test_delete_nonexistent_task():
    response = schema.execute_sync(
        """
        mutation DeleteTask($taskId: Int!) {
            deleteTask(taskId: $taskId)
        }
        """,
        variable_values={"taskId": 9999},
    )
    assert response.errors
    assert "does not exist" in str(response.errors[0])


@pytest.mark.django_db
def test_create_task_missing_title():
    response = schema.execute_sync(
        """
        mutation CreateTask($data: TaskInput!) {
            createTask(data: $data) {
                id
                title
            }
        }
        """,
        variable_values={"data": {"description": "Missing title", "completed": False}},
    )
    assert response.errors
    assert "title" in str(response.errors[0]).lower()


@pytest.mark.django_db
def test_create_task_default_completed():
    response = schema.execute_sync(
        """
        mutation CreateTask($data: TaskInput!) {
            createTask(data: $data) {
                id
                title
                completed
            }
        }
        """,
        variable_values={
            "data": {"title": "Default Completed", "description": "Check default"}
        },
    )
    task_data = response.data["createTask"]
    assert task_data["completed"] is False
