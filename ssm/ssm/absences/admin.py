from django.contrib import admin
from reversion.admin import VersionAdmin

from ssm.absences.models import Absence


@admin.register(Absence)
class AbsenseAdmin(VersionAdmin):
    list_display = ['reason', 'status', 'user', 'start_date', 'end_date']
    list_filter = ['reason', 'status']
    search_fields = ['start_date', 'end_date']
    fieldsets = [
        (None, {'fields': ['decision_by']}),
        ('Details', {'fields': ['user', 'reason', 'status', 'start_date', 'end_date', 'notes']})
    ]
    filter_horizontal = []
