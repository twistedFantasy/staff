from django_filters.rest_framework import FilterSet, CharFilter

from ssm.users.models import User
from ssm.core.filters import ObjectFieldFilterBackend


class UserFilter(FilterSet):
    name = CharFilter(field_name='full_name', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['email', 'name', 'full_name', 'date_of_birth']


class UserFilterBackend(ObjectFieldFilterBackend):
    filter_field = 'user_id'
