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
        read_only_fields = []


class MembersSerializer(StaffMembersSerializer):

    class Meta(StaffMembersSerializer.Meta):
        read_only_fields = ['user', 'project', 'role', 'hours_per_day', 'joined_date', 'left_date']


class ProjectSerializer(StaffProjectSerializer):

    class Meta(StaffProjectSerializer.Meta):
        read_only_fields = [
            'name', 'description', 'specification', 'start_date', 'end_date', 'status', 'members',
            'estimation_in_man_hours',
        ]
