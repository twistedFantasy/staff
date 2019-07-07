from django.contrib import admin

from ssm.assessments.models import Assessment, Checkpoint, Task


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'start_date', 'end_date']
    search_fields = ['start_date', 'end_date']
    fieldsets = [
        (None, {'fields': ['decision_by']}),
        ('Details', {'fields': ['user', 'status', 'start_date', 'end_date', 'plan', 'comments', 'notes']})
    ]
    filter_horizontal = []


@admin.register(Checkpoint)
class CheckpointAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'date']
    search_fields = ['date']
    fieldsets = [
        (None, {'fields': ['assessment', 'title', 'date']})
    ]
    filter_horizontal = []


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['checkpoint', 'title', 'completed']
    search_fields = ['title', 'description']
    fieldsets = [
        (None, {'fields': ['checkpoint', 'title', 'description', 'completed']})
    ]
    filter_horizontal = []
