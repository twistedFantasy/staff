from django_filters.rest_framework import FilterSet

from ssm.absences.models import Absence


class AbsenceFilter(FilterSet):

    class Meta:
        model = Absence
        fields = ['reason', 'status', 'start_date', 'end_date']
