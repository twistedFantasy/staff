from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from ssm.projects.models import Project
from ssm.projects.serializers import ProjectSerializer
from ssm.projects.permissions import IsProjectMemberOrStaff
from ssm.projects.filters import ProjectFilterBackend
from ssm.core.permissions import ReadOnlyOrStaff


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectMemberOrStaff, ReadOnlyOrStaff]
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend, ProjectFilterBackend]
    search_fields = ['name', 'customer__full_name']
    ordering_fields = ['name']
    filter_fields = ['customer__full_name']
    ordering = ['name']
