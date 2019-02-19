from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from ssm.absences.models import Absence, STATUS, BLOCKED_STATUSES
from ssm.absences.filters import AbsenceFilter
from ssm.absences.serializers import AbsenceSerializer
from ssm.users.filters import UserFilterBackend
from ssm.core.permissions import IsObjectOwnerOrStaffObjectPermission


class AbsenceViewSet(ModelViewSet):
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerOrStaffObjectPermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter, UserFilterBackend]
    filterset_class = AbsenceFilter

    def create(self, request, *args, **kwargs):
        self._force_create_permissions(request)
        return super().create(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        self._check_update_permissions(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._check_update_permissions(request)
        return super().partial_update(request, *args, **kwargs)

    def _force_create_permissions(self, request):
        if not request.user.is_staff:
            request.data['user'] = request.user.id
            request.data['status'] = STATUS.new
            request.data['approved_by'] = None

    def _check_update_permissions(self, request):
        if 'status' in request.data and not request.user.is_staff and self.get_object().status in BLOCKED_STATUSES:
            raise PermissionDenied
