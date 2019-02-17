from rest_framework.serializers import ModelSerializer
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin

from ssm.projects.models import Project, MembershipModel
from ssm.users.models import User


class MembershipSerializer(ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.full_name')

    class Meta:
        model = MembershipModel
        fields = ['user_name', 'role', 'hours_per_day']
        read_only = ['user_name']


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['full_name']
        read_only = ['full_name']


class ProjectSerializer(DynamicFieldsMixin, ModelSerializer):
    members = MembershipSerializer(source='membershipmodel_set', many=True, read_only=True)
    customer = CustomerSerializer(many=False, read_only=True)

    class Meta:
        model = Project
        fields = ['name', 'description', 'specification', 'customer', 'members']
        read_only_fields = ['id']
