from rest_framework import permissions


class IsProjectMemberOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        return True if request.user.is_staff else request.user.membershipmodel_set.filter(project=obj).exists()


class ReadOnlyOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return True if request.user.is_staff else request.method in permissions.SAFE_METHODS
