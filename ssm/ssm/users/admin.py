from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from ssm.skills.models import UserSkillModel
from ssm.users.models import User
from ssm.users.tasks.assessment import Assessment
from ssm.core.decorators import message_user


class UserSkillInline(admin.TabularInline):
    model = UserSkillModel
    extra = 1


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
        ('Assessment', {'fields': ['assessment_date', 'assessment_plan']}),
        ('Permissions', {'fields': ['is_active', 'is_staff', 'is_superuser']}),
        ('System', {'classes': ['collapse'], 'fields': ['created', 'modified']}),
    ]
    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['email', 'password1', 'password2']}
         ),
    ]
    inlines = [UserSkillInline]
    ordering = ['-modified']
    filter_horizontal = []
    show_full_result_count = False
    actions = ['notify_users']

    @message_user("Notified!")
    def notify_users(self, request, queryset):
        Assessment.delay()
    notify_users.short_description = 'Notify employers about assessment'


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
