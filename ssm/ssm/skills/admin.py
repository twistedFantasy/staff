from django.contrib import admin

from ssm.skills.models import Skill, Verification


class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['category']
    search_fields = ['name']
    fieldsets = [
        (None, {'fields': ['name', 'category']})
    ]


class VerificationAdmin(admin.ModelAdmin):
    list_display = ['question', 'skill']
    search_fields = ['question']
    fieldsets = [
        (None, {'fields': ['question', 'answer']})
    ]


admin.site.register(Skill, SkillAdmin)
admin.site.register(Verification, VerificationAdmin)
