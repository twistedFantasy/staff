from rest_framework.permissions import BasePermission

from ssm.core.permissions import IsAllowedMethodOrStaff


class UserCustomIsAllowedMethodOrStaff(IsAllowedMethodOrStaff):
    methods = ['GET', 'HEAD', 'OPTIONS', 'PATCH']


class AbsenceCustomIsAllowedMethodOrStaff(IsAllowedMethodOrStaff):
    methods = ['GET', 'HEAD', 'OPTIONS', 'POST', 'PATCH', 'DELETE']


class IsCurrentUserOrStaff(BasePermission):
    """
        Custom permission to allow correct access based on if it's staff or simple user
    """
    def has_object_permission(self, request, view, obj):
        return True if request.user.is_staff else request.user == obj
