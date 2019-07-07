from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ssm.assessments.models import Assessment, Checkpoint, Task
from ssm.assessments.serializers import StaffAssessmentSerializer, AssessmentSerializer, StaffCheckpointSerializer, \
    CheckpointSerializer, StaffTaskSerializer, TaskSerializer
from ssm.assessments.filters import CheckpointFilterBackend, TaskFilterBackend
from ssm.users.filters import UserFilterBackend
from ssm.core.permissions import IsAllowedMethodOrStaff, IsObjectOwnerOrStaff


class AssessmentViewSet(ModelViewSet):
    queryset = Assessment.objects.all()
    permission_classes = [IsAuthenticated, IsAllowedMethodOrStaff, IsObjectOwnerOrStaff]
    filter_backends = [UserFilterBackend, DjangoFilterBackend, OrderingFilter]
    search_fields = ['status', 'start_date', 'end_date']

    def get_serializer_class(self):
        return StaffAssessmentSerializer if self.request.user.is_staff else AssessmentSerializer


class CheckpointViewSet(ModelViewSet):
    queryset = Checkpoint.objects.all()
    permission_classes = [IsAuthenticated, IsAllowedMethodOrStaff]
    filter_backends = [CheckpointFilterBackend, DjangoFilterBackend, OrderingFilter]

    def get_serializer_class(self):
        return StaffCheckpointSerializer if self.request.user.is_staff else CheckpointSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsObjectOwnerOrStaff]
    filter_backends = [TaskFilterBackend, DjangoFilterBackend, OrderingFilter]

    def get_serializer_class(self):
        return StaffTaskSerializer if self.request.user.is_staff else TaskSerializer
