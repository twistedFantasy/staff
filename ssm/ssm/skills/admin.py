from django.contrib import admin

from ssm.skills.models import Skill, Verification


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['category']
    search_fields = ['name']
    fieldsets = [
        (None, {'fields': ['name', 'category']})
    ]


@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ['question', 'skill']
    search_fields = ['question']
    fieldsets = [
        (None, {'fields': ['skill', 'question', 'answer']})
    ]
