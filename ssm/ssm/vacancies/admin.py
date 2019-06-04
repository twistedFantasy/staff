from django.contrib import admin

from ssm.vacancies.models import Vacancy


class VacancyAdmin(admin.ModelAdmin):
    list_display = ['position', 'bonus', 'status']
    search_fields = ['position', 'description']
    fieldsets = [
        (None, {'fields': ['position', 'description', 'bonus', 'status', 'start_date', 'end_date', 'recommended_by']})
    ]


admin.site.register(Vacancy, VacancyAdmin)
