from django.contrib import admin

from ssm.events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'active']
    search_fields = ['start_date', 'end_date']
    fieldsets = [
        (None, {'fields': ['title', 'description', 'start_date', 'end_date', 'active']})
    ]
