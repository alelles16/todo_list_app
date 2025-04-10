from rest_framework import serializers
from core.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    """

    class Meta:
        model = Task
        fields = ("id", "title", "description", "completed")
        read_only_fields = ("created_at", "updated_at")
        extra_kwargs = {
            "title": {"required": True, "allow_blank": False},
            "description": {"required": True, "allow_blank": False},
        }
