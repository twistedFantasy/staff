from django.contrib import admin
from reversion.admin import VersionAdmin

from ssm.projects.models import Project, MembersModel, Vacancy
from ssm.projects.mixins import ProjectAdminMixin


class MembersInline(admin.TabularInline):
    model = MembersModel


@admin.register(Project)
class ProjectAdmin(VersionAdmin, ProjectAdminMixin):
    list_display = ['name', 'status', 'get_members_count']
    list_filter = ['status']
    search_fields = ['name']
    readonly_fields = ['vacancies_url']
    fieldsets = [
        (None, {'fields': ['name', 'link', 'description', 'task_examples', 'technology_stack', 'vacancies_url']}),
        ('Details', {'fields': ['status', 'estimation_in_man_hours', 'specification']}),
        ('Duration', {'fields': ['start_date', 'end_date']}),
    ]
    inlines = [MembersInline]

    def get_members_count(self, obj):
        return obj.members.filter(membersmodel__left_date=None).count()
    get_members_count.short_description = 'Members'


@admin.register(Vacancy)
class VacancyAdmin(VersionAdmin):
    list_display = ['level', 'project', 'priority', 'count', 'active']
    list_filter = ['priority', 'active']
    search_fields = ['level', 'requirements']
    fieldsets = [
        (None, {'fields': ['project']}),
        ('Details', {'fields': ['level', 'priority', 'requirements', 'count', 'active']}),
    ]
    filter_horizontal = []
