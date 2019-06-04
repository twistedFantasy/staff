from rest_framework.serializers import ReadOnlyField, ModelSerializer
from drf_dynamic_fields import DynamicFieldsMixin

from ssm.projects.models import Project, MembersModel


class StaffMembersSerializer(ModelSerializer):
    user_name = ReadOnlyField(source='user.full_name')

    class Meta:
        model = MembersModel
        fields = ['user_name', 'role', 'hours_per_day']


class MembersSerializer(StaffMembersSerializer):

    class Meta(StaffMembersSerializer.Meta):
        read_only_fields = ['user', 'project', 'role', 'hours_per_day', 'joined_date', 'left_date']


class StaffProjectSerializer(DynamicFieldsMixin, ModelSerializer):

    class Meta:
        model = Project
        fields = ['name', 'description', 'specification', 'customer', 'members']


class ProjectSerializer(StaffProjectSerializer):

    class Meta(StaffProjectSerializer.Meta):
        read_only_fields = [
            'name', 'description', 'specification', 'start_date', 'end_date', 'status', 'members',
            'estimation_in_man_hours',
        ]


class StaffProjectWithMembersSerializer(StaffProjectSerializer):
    members = StaffMembersSerializer(source='user_set', many=True)

    class Meta(StaffProjectSerializer.Meta):
        pass


class ProjectWithMembersSerialize(ProjectSerializer):
    members = MembersSerializer(source='user_set', many=True, read_only=True)

    class Meta(ProjectSerializer.Meta):
        read_only_fields = ProjectSerializer.Meta.read_only_fields + ['members']
