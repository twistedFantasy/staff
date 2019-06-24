from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from ssm.skills.models import UserSkillModel
from ssm.projects.models import MembersModel
from ssm.users.models import User


class UserSkillInline(admin.TabularInline):
    model = UserSkillModel
    extra = 1


class UserProjectInline(admin.TabularInline):
    model = MembersModel


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['email', 'full_name', 'is_active', 'modified']
    list_filter = ['is_staff', 'is_superuser']
    search_fields = ['email', 'full_name']
    readonly_fields = ['created', 'modified']
    fieldsets = [
        (None, {'fields': ['email', 'password']}),
        ('Details', {'fields': [
            'full_name', 'ld_number', 'position', 'date_of_birth', 'hired_date', 'end_of_contract',
            'education', 'phone_number', 'phone_number2', 'has_card', 'has_key', 'skype',
            'working_hours',
        ]}),
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
    actions = ['notify_users']


admin.site.unregister(Group)
