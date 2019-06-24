from rest_framework.permissions import BasePermission

from ssm.absences.models import REASON, STATUS
from ssm.core.permissions import IsAllowedMethodOrStaff


class AbsenceIsAllowedMethodOrStaff(IsAllowedMethodOrStaff):
    methods = ['GET', 'HEAD', 'OPTIONS', 'POST', 'PATCH']


class AbsencePermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_staff:
            if request.method == 'POST' or request.method == 'PATCH':
                if 'user' in request.data and request.user.id != request.data['user']['id']:
                    return False
                if 'reason' in request.data and request.data['reason'] == REASON.holiday:
                    return False
            if request.method == 'POST':
                if 'status' in request.data and request.data['status'] != STATUS.new:
                    return False
        return True
