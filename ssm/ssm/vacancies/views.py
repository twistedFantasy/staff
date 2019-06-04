from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ssm.vacancies.models import Vacancy
from ssm.vacancies.serializers import StaffVacancySerializer, VacancySerializer
from ssm.core.permissions import IsAllowedMethodOrStaff


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()
    permission_classes = [IsAuthenticated, IsAllowedMethodOrStaff]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ['position', 'description']
    ordering_fields = ['start_date', 'end_date']

    def get_serializer_class(self):
        return StaffVacancySerializer if self.request.user.is_staff else VacancySerializer
