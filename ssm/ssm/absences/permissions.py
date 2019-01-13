from rest_framework.permissions import BasePermission


class IsAbsenceOwnerOrStaff(BasePermission):

    def has_object_permission(self, request, view, obj):
        return True if request.user.is_staff else request.user == obj.user
