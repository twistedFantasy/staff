from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ssm.absences.models import Absence, REASON
from ssm.absences.filters import AbsenceFilter
from ssm.absences.permissions import AbsenceIsAllowedMethodOrStaff, AbsencePermission
from ssm.absences.serializers import StaffAbsenceSerializer, AbsenceSerializer
from ssm.core.permissions import IsObjectOwnerOrStaff


class AbsenceViewSet(ModelViewSet):
    queryset = Absence.objects.all()
    permission_classes = [IsAuthenticated, AbsenceIsAllowedMethodOrStaff,  IsObjectOwnerOrStaff, AbsencePermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AbsenceFilter

    def get_serializer_class(self):
        return StaffAbsenceSerializer if self.request.user.is_staff else AbsenceSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Absence.objects.all()
        return Absence.objects.filter(Q(user=self.request.user) | Q(reason=REASON.holiday))
