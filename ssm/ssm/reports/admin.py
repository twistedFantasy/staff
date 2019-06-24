from django import forms
from django.contrib import admin
from django.contrib.admin.helpers import ActionForm

from ssm.reports.models import Report, History
from ssm.core.decorators import message_user


class ReportActionForm(ActionForm):
    start = forms.DateField(required=False)
    end = forms.DateField(required=False)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    action_form = ReportActionForm
    list_display = ['name']
    search_fields = ['name', 'description']
    fieldsets = [
        (None, {'fields': ['uid', 'name', 'description']})
    ]
    ordering = ['name']
    filter_horizontal = []
    actions = ['launch']

    @message_user("Launched selected reports")
    def launch(self, request, queryset):
        start, end = request.POST['start'], request.POST['end']  #Day(request.POST['start']), Day(request.POST['end'])
        for report in queryset:
            report.launch(start, end)
    launch.short_description = 'Launch reports'


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'report', 'status']
    search_fields = ['report']
    fieldsets = [
        (None, {'fields': ['report', 'status', 'path', 'params', 'msg', 'task_id']})
    ]
    ordering = ['-id']
    filter_horizontal = []
    list_select_related = ['report']
