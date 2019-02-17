from django.contrib import admin

from ssm.projects.models import Project, MembershipModel


class MembershipInline(admin.TabularInline):
    model = MembershipModel


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'customer', 'get_members_count']
    search_fields = ['name']
    fieldsets = [
        (None, {'fields': ['name', 'description', 'specification', 'status', 'customer', 'estimation_in_man_hours']}),
        ('Duration', {'fields': ['start_date', 'end_date']}),
    ]
    inlines = [MembershipInline]
    list_filter = ['customer']

    def get_members_count(self, obj):
        return len(obj.members.filter(membershipmodel__date_left=None))
    get_members_count.short_description = 'Team size'


admin.site.register(Project, ProjectAdmin)
