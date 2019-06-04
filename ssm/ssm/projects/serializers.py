from rest_framework.serializers import ReadOnlyField, ModelSerializer
from drf_dynamic_fields import DynamicFieldsMixin

from ssm.projects.models import Project, MembersModel


class StaffMembersSerializer(ModelSerializer):
    user_name = ReadOnlyField(source='user.full_name')

    class Meta:
        model = MembersModel
        fields = ['user_name', 'role', 'hours_per_day']


class StaffProjectSerializer(DynamicFieldsMixin, ModelSerializer):
    members = StaffMembersSerializer(source='membersmodel_set', many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['name', 'description', 'specification', 'customer', 'members']
        read_only_fields = ['id']


class MembersSerializer(StaffMembersSerializer):

    class Meta(StaffMembersSerializer.Meta):
        read_only_fields = '__all__'


class ProjectSerializer(StaffProjectSerializer):

    class Meta(StaffProjectSerializer.Meta):
        read_only_fields = '_all__'
