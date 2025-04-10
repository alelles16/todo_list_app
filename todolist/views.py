from django.http import Http404
from rest_framework import viewsets
from rest_framework.exceptions import NotFound

from core.models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """

    queryset = Task.objects.all().order_by("-created_at")
    serializer_class = TaskSerializer

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail="Tasks not found.")
