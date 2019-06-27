from django.contrib import admin

from ssm.absences.models import Absence


@admin.register(Absence)
class AbsenseAdmin(admin.ModelAdmin):
    list_display = ['reason', 'status', 'user', 'start_date', 'end_date']
    search_fields = ['start_date', 'end_date']
    fieldsets = [
        (None, {'fields': ['decision_by']}),
        ('Details', {'fields': ['user', 'reason', 'status', 'start_date', 'end_date', 'notes']})
    ]
    filter_horizontal = []
