from django.utils.safestring import mark_safe

from ssm.core.mixins import BaseAdminMixin


class UserAdminMixin(BaseAdminMixin):

    def absences_url(self, obj):
        from ssm.absences.models import Absence
        return self.get_url(Absence, singular='absence', plural='absences', user=obj.id)
    absences_url.short_description = 'Absences'

    def assessments_url(self, obj):
        from ssm.assessments.models import Assessment
        return self.get_url(Assessment, singular='assessment', plural='assessments', user=obj.id)
    assessments_url.short_description = 'Assessments'

    def display_color(self, obj):
        return mark_safe(f'<b style="background:{obj.color};">.....</b>')
    display_color.short_description = 'Color'

    def current_workload(self, obj):
        return obj.current_workload()
    current_workload.short_description = 'Workload'
