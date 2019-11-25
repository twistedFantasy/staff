from django.contrib import admin
from reversion.admin import VersionAdmin

from ssm.events.models import Event


@admin.register(Event)
class EventAdmin(VersionAdmin):
    list_display = ['title', 'start_date', 'end_date', 'active']
    list_filter = ['active']
    search_fields = ['start_date', 'end_date']
    fieldsets = [
        (None, {'fields': ['title', 'description', 'start_date', 'end_date', 'active']})
    ]
