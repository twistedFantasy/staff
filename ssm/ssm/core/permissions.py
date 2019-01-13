from rest_framework.permissions import BasePermission


class ReadOnlyOrStaff(BasePermission):

    def has_permission(self, request, view):
        return True if request.user.is_staff else request.method in ('GET', 'HEAD', 'OPTIONS', 'PATCH', 'DELETE')
