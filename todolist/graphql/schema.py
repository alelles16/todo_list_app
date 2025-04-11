import strawberry
from dataclasses import asdict
from strawberry_django.optimizer import DjangoOptimizerExtension

from .types import TaskType, TaskInput, TaskUpdateInput
from core.models import Task


@strawberry.type
class Query:

    @strawberry.field
    def tasks(self) -> list[TaskType]:
        return list(Task.objects.order_by("-created_at"))

    @strawberry.field
    def task(self, id: int) -> TaskType:
        try:
            return Task.objects.get(pk=id)
        except Task.DoesNotExist:
            raise ValueError(f"Task with ID {id} was not found.")


@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_task(self, data: TaskInput) -> TaskType:
        return Task.objects.create(**asdict(data))

    @strawberry.mutation
    def update_task(self, task_id: int, data: TaskUpdateInput) -> TaskType:
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise ValueError(f"Task with ID {task_id} does not exist.")

        for field, value in asdict(data).items():
            if value is not None:
                setattr(task, field, value)

        task.save()
        return task

    @strawberry.mutation
    def delete_task(self, task_id: int) -> bool:
        try:
            task = Task.objects.get(pk=task_id)
            task.delete()
            return True
        except Task.DoesNotExist:
            raise ValueError(f"Task with ID {task_id} does not exist.")


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[DjangoOptimizerExtension],
)
