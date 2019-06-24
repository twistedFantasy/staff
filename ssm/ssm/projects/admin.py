from django.contrib import admin

from ssm.projects.models import Project, MembersModel


class MembersInline(admin.TabularInline):
    model = MembersModel


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'get_members_count']
    search_fields = ['name']
    fieldsets = [
        (None, {'fields': ['name', 'description']}),
        ('Details', {'fields': ['status', 'estimation_in_man_hours', 'specification']}),
        ('Duration', {'fields': ['start_date', 'end_date']}),
    ]
    inlines = [MembersInline]

    def get_members_count(self, obj):
        return obj.members.filter(membersmodel__left_date=None).count()
    get_members_count.short_description = 'Members'
