from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from ssm.projects.models import Project
from ssm.projects.serializers import StaffProjectSerializer, ProjectSerializer, StaffProjectWithMembersSerializer, \
    ProjectWithMembersSerialize
from ssm.projects.permissions import IsProjectMemberOrStaff
from ssm.projects.filters import ProjectFilterBackend
from ssm.core.permissions import IsAllowedMethodOrStaff


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsAllowedMethodOrStaff, IsProjectMemberOrStaff]
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend, ProjectFilterBackend]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if 'members' in self.request.query_params:
            return StaffProjectWithMembersSerializer if self.request.user.is_staff else ProjectWithMembersSerialize
        return StaffProjectSerializer if self.request.user.is_staff else ProjectSerializer
