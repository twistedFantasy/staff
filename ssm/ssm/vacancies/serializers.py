from rest_framework.serializers import ModelSerializer

from ssm.vacancies.models import Vacancy
from ssm.users.serializers import ByUserSerializer


class StaffVacancySerializer(ModelSerializer):
    recommended_by = ByUserSerializer(required=False)

    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancySerializer(ModelSerializer):

    class Meta(StaffVacancySerializer.Meta):
        read_only_fields = '__all__'
