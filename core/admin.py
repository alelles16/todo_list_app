from django.contrib import admin
from core.models import Task


class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface for the Task model.
    """

    list_display = ("id", "title", "completed", "created_at", "updated_at")
    search_fields = ("title",)
    list_filter = ("completed",)
    ordering = ("-created_at",)


admin.site.register(Task, TaskAdmin)
