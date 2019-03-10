from django.contrib import admin

from ssm.projects.models import Project, MembersModel


class MembersInline(admin.TabularInline):
    model = MembersModel


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'customer', 'get_members_count']
    search_fields = ['name']
    fieldsets = [
        (None, {'fields': ['name', 'customer', 'description']}),
        ('Details', {'fields': ['status', 'estimation_in_man_hours', 'specification']}),
        ('Duration', {'fields': ['start_date', 'end_date']}),
    ]
    inlines = [MembersInline]
    list_filter = ['customer']

    def get_members_count(self, obj):
        return obj.members.filter(membersmodel__left_date=None).count()
    get_members_count.short_description = 'Members'


admin.site.register(Project, ProjectAdmin)
