from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ssm.assessments.models import Assessment
from ssm.assessments.serializers import StaffAssessmentSerializer, AssessmentSerializer
from ssm.users.filters import UserFilterBackend
from ssm.core.permissions import IsAllowedMethodOrStaff, IsObjectOwnerOrStaff


class AssessmentViewSet(ModelViewSet):
    queryset = Assessment.objects.all()
    permission_classes = [IsAuthenticated, IsAllowedMethodOrStaff, IsObjectOwnerOrStaff]
    filter_backends = [UserFilterBackend, DjangoFilterBackend, OrderingFilter]
    search_fields = ['status', 'start_date', 'end_date']

    def get_serializer_class(self):
        return StaffAssessmentSerializer if self.request.user.is_staff else AssessmentSerializer