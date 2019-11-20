from django.contrib import admin

from ssm.skills.models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['category']
    search_fields = ['name']
    fieldsets = [
        (None, {'fields': ['name', 'category']})
    ]
