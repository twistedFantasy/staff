from django.contrib import admin
from reversion.admin import VersionAdmin

from ssm.skills.models import Skill


@admin.register(Skill)
class SkillAdmin(VersionAdmin):
    list_display = ['name']
    list_filter = ['category']
    search_fields = ['name']
    fieldsets = [
        (None, {'fields': ['name', 'category']})
    ]
