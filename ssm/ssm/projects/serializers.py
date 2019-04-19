from rest_framework.serializers import ReadOnlyField, ModelSerializer
from drf_dynamic_fields import DynamicFieldsMixin

from ssm.projects.models import Project, MembersModel
from ssm.users.models import User


class MembersSerializer(ModelSerializer):
    user_name = ReadOnlyField(source='user.full_name')

    class Meta:
        model = MembersModel
        fields = ['user_name', 'role', 'hours_per_day']
        read_only = ['user_name']


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['full_name']
        read_only = ['full_name']


class ProjectSerializer(DynamicFieldsMixin, ModelSerializer):
    members = MembersSerializer(source='membersmodel_set', many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['name', 'description', 'specification', 'customer', 'members']
        read_only_fields = ['id']
