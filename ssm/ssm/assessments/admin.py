from django.contrib import admin

from ssm.assessments.models import Assessment


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'start_date', 'end_date']
    search_fields = ['start_date', 'end_date']
    fieldsets = [
        (None, {'fields': ['decision_by']}),
        ('Details', {'fields': ['user', 'status', 'start_date', 'end_date', 'plan', 'comments', 'notes']})
    ]
    filter_horizontal = []
