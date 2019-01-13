from django.contrib import admin

from ssm.absences.models import Absence


class AbsenseAdmin(admin.ModelAdmin):
    list_display = ['reason', 'status', 'user', 'start_date', 'end_date']
    search_fields = ['start_date', 'end_date']
    fieldsets = [
        (None, {'fields': ['approved_by']}),
        ('Details', {'fields': ['user', 'reason', 'status', 'start_date', 'end_date', 'notes']})
    ]
    filter_horizontal = []


admin.site.register(Absence, AbsenseAdmin)
