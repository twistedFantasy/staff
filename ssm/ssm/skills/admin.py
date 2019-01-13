from django.contrib import admin

from ssm.skills.models import Skill


class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['category']
    fieldsets = [
        (None, {'fields': ['name', 'category']})
    ]


admin.site.register(Skill, SkillAdmin)
