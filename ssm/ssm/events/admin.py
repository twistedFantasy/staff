from django.contrib import admin

from ssm.events.models import Event, FAQ


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'active']
    search_fields = ['start_date', 'end_date']
    fieldsets = [
        (None, {'fields': ['title', 'description', 'start_date', 'end_date', 'active']})
    ]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'active']
    search_fields = ['question', 'answer']
    fieldsets = [
        (None, {'fields': ['question', 'answer', 'order', 'active']})
    ]
