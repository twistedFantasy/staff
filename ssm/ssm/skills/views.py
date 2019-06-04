from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ssm.skills.models import Skill
from ssm.skills.filters import SkillFilterBackend
from ssm.skills.serializers import StaffSkillSerializer, SkillSerializer, StaffSkillWithUsersSerializer, \
    SkillWithUsersSerializer
from ssm.core.permissions import IsAllowedMethodOrStaff


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    permission_classes = [IsAuthenticated, IsAllowedMethodOrStaff]
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend, SkillFilterBackend]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if 'users' in self.request.query_params:
            return StaffSkillWithUsersSerializer if self.request.user.is_staff else SkillWithUsersSerializer
        return StaffSkillSerializer if self.request.user.is_staff else SkillSerializer
