from ssm.core.mixins import BaseAdminMixin

from ssm.projects.models import Vacancy


class ProjectAdminMixin(BaseAdminMixin):

    def vacancies_url(self, obj):
        return self.get_url(Vacancy, singular='vacancy', plural='vacancies', project=obj.id)
    vacancies_url.short_description = 'Vacancies'
