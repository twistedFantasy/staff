from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND


from ssm.users.models import User, Absence, Assessment, ABSENCE_STATUS, ABSENCE_BLOCKED_STATUSES
from ssm.users.filters import UserFilter, UserFilterBackend, AbsenceFilter
from ssm.users.serializers import StaffUserSerializer, UserSerializer, StaffUserWithSkillsSerializer, \
    UserWithSkillsSerializer, SSMTokenObtainPairSerializer, AbsenceSerializer, StaffAbsenceSerializer, \
    StaffAssessmentSerializer, AssessmentSerializer
from ssm.users.permissions import AbsenceCustomIsAllowedMethodOrStaff, UserCustomIsAllowedMethodOrStaff, \
    IsCurrentUserOrStaff
from ssm.core.filters import ObjectFieldFilterBackend
from ssm.core.permissions import IsAllowedMethodOrStaff, IsObjectOwnerOrStaff
from ssm.core.views import CustomTokenObtainPairView


class SSMTokenObtainPairView(CustomTokenObtainPairView):
    user = User
    serializer_class = SSMTokenObtainPairSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().prefetch_related('skills')
    permission_classes = [IsAuthenticated, UserCustomIsAllowedMethodOrStaff, IsCurrentUserOrStaff]
    filter_backends = [ObjectFieldFilterBackend, SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = UserFilter
    search_fields = ['email', 'full_name']
    ordering_fields = ['email', 'full_name']
    ordering = ['email']

    def get_serializer_class(self):
        if 'skills' not in self.request.query_params or self.request.query_params.get('skills') == 'true':
            return StaffUserWithSkillsSerializer if self.request.user.is_staff else UserWithSkillsSerializer
        return StaffUserSerializer if self.request.user.is_staff else UserSerializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        password = request.data.get('password')
        if not password:
            return Response({'msg': 'password param required'}, status=HTTP_404_NOT_FOUND)
        request.user.set_password(password)
        request.user.save(update_fields=['password'])
        return Response({'msg': 'password successfully updated'}, status=HTTP_200_OK)


class AbsenceViewSet(ModelViewSet):
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer
    permission_classes = [IsAuthenticated, AbsenceCustomIsAllowedMethodOrStaff, IsObjectOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, OrderingFilter, UserFilterBackend]
    filterset_class = AbsenceFilter

    def get_serializer_class(self):
        return StaffAbsenceSerializer if self.request.user.is_staff else AbsenceSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            request.data['user'] = request.user.id
            request.data['status'] = ABSENCE_STATUS.new
            request.data['approved_by'] = None
        return super().create(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        self._check_update_permissions(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._check_update_permissions(request)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.get_object().status in ABSENCE_BLOCKED_STATUSES or self.get_object().approved_by:
            raise PermissionDenied
        return super.destroy(request, *args, **kwargs)

    def _check_update_permissions(self, request):
        if 'status' in request.data and not request.user.is_staff and self.get_object().status in ABSENCE_BLOCKED_STATUSES:
            raise PermissionDenied


class AssessmentViewSet(ModelViewSet):
    queryset = Assessment.objects.all()
    permission_classes = [IsAuthenticated, IsAllowedMethodOrStaff, IsObjectOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ['status', 'start_date', 'end_date']

    def get_serializer_class(self):
        return StaffAssessmentSerializer if self.request.user else AssessmentSerializer
