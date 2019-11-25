from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from reversion.admin import VersionAdmin

from ssm.skills.models import UserSkillModel
from ssm.projects.models import MembersModel
from ssm.users.models import User
from ssm.users.mixins import UserAdminMixin


class UserSkillInline(admin.TabularInline):
    model = UserSkillModel
    extra = 1


class UserProjectInline(admin.TabularInline):
    model = MembersModel


@admin.register(User)
class UserAdmin(UserAdmin, VersionAdmin, UserAdminMixin):
    list_display = ['email', 'full_name', 'level', 'display_color', 'current_workload', 'is_active', 'modified']
    list_filter = ['level', 'color', 'is_staff', 'is_superuser']
    search_fields = ['email', 'full_name']
    readonly_fields = ['absences_url', 'assessments_url', 'created', 'modified']
    fieldsets = [
        (None, {'fields': ['email', 'password', 'mentor', 'level', 'color']}),
        ('Details', {'fields': [
            'full_name', 'ld_number', 'position', 'date_of_birth', 'hired_date', 'end_of_contract',
            'education', 'phone_number', 'phone_number2', 'has_card', 'has_key', 'has_key2', 'has_key3', 'skype',
            'working_hours',
        ]}),
        ('Relationships', {'fields': ['absences_url', 'assessments_url']}),
        ('Permissions', {'fields': ['is_active', 'is_staff', 'is_superuser']}),
        ('System', {'classes': ['collapse'], 'fields': ['created', 'modified']}),
    ]
    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['email', 'password1', 'password2']}
         ),
    ]
    inlines = [UserSkillInline, UserProjectInline]
    ordering = ['-modified']
    filter_horizontal = []
    show_full_result_count = False
    actions = []


admin.site.unregister(Group)
