from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff


class ReadOnlyOrStaff(BasePermission):

    def has_permission(self, request, view):
        return True if request.user.is_staff else request.method in ('GET', 'HEAD', 'OPTIONS', 'PATCH', 'DELETE')


class IsObjectOwnerOrStaffObjectPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return True if request.user.is_staff else request.user == obj.user
