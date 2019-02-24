from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from ssm.users.models import User
from ssm.users.filters import UserFilter
from ssm.users.serializers import UserWithSkillsSerializer, SSMTokenObtainPairSerializer
from ssm.users.permissions import IsCurrentUserOrStaff
from ssm.core.permissions import ReadOnlyOrStaff
from ssm.core.filters import ObjectFieldFilterBackend
from ssm.core.views import CustomTokenObtainPairView


class SSMTokenObtainPairView(CustomTokenObtainPairView):
    user = User
    serializer_class = SSMTokenObtainPairSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().prefetch_related('skills')
    serializer_class = UserWithSkillsSerializer
    permission_classes = [IsAuthenticated, ReadOnlyOrStaff, IsCurrentUserOrStaff]
    filter_backends = [ObjectFieldFilterBackend, SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = UserFilter
    search_fields = ['email', 'full_name']
    ordering_fields = ['email', 'full_name']
    ordering = ['email']


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        password = request.data.get('password')
        if not password:
            return Response({'msg': 'password param required'}, status=HTTP_404_NOT_FOUND)
        request.user.set_password(password)
        request.user.save(update_fields=['password'])
        return Response({'msg': 'password successfully updated'}, status=HTTP_200_OK)