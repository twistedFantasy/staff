from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from ssm.absences.models import Absence
from ssm.absences.filters import AbsenceFilter
from ssm.absences.permissions import IsAbsenceOwnerOrStaff
from ssm.absences.serializers import AbsenceSerializer
from ssm.users.filters import UserFilterBackend


class AbsenceViewSet(ModelViewSet):
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer
    permission_classes = [IsAbsenceOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, OrderingFilter, UserFilterBackend]
    filterset_class = AbsenceFilter

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.data['user'] if request.user.is_staff else request.user.id
        return super().create(request, args, kwargs)
