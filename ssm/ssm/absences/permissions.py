from rest_framework.permissions import BasePermission

from ssm.absences.models import REASON, STATUS
from ssm.core.permissions import IsAllowedMethodOrStaff


class AbsenceIsAllowedMethodOrStaff(IsAllowedMethodOrStaff):
    methods = ['GET', 'HEAD', 'OPTIONS', 'POST', 'PATCH']


class AbsencePermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_staff:
            data = request.data
            if request.method == 'POST':
                if 'user' not in data or request.user.id != data['user']['id']:
                    return False
                if 'reason' not in data or ('user' in data and data['reason'] == REASON.holiday):
                    return False
                if 'status' not in data or data['status'] != STATUS.new:
                    return False
            elif request.method == 'PATCH':
                if 'user' in data and request.user.id != data['user']['id']:
                    return False
                if 'reason' in data and data['reason'] == REASON.holiday:
                    return False
        return True
