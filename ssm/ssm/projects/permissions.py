from rest_framework import permissions


class IsProjectMemberOrStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return True if request.user.is_staff else request.user.membersmodel_set.filter(project=obj).exists()
