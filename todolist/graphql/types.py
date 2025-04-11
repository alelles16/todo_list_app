import strawberry_django

from core.models import Task


@strawberry_django.type(Task)
class TaskType:
    id: int
    title: str
    description: str
    completed: bool


@strawberry_django.input(Task)
class TaskInput:
    title: str
    description: str
    completed: bool = False


@strawberry_django.input(Task)
class TaskUpdateInput:
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
