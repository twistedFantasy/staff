from rest_framework.serializers import ModelSerializer
from drf_dynamic_fields import DynamicFieldsMixin

from ssm.users.models import User
from ssm.skills.serializers import SkillSerializer
from ssm.projects.serializers import MembershipSerializer
from ssm.core.serializers import CustomTokenObtainPairSerializer


class SSMTokenObtainPairSerializer(CustomTokenObtainPairSerializer):
    pass


class UserSerializer(DynamicFieldsMixin, ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = User
        depth = 1
        fields = [
            'email', 'is_staff', 'full_name', 'date_of_birth', 'education', 'phone_number', 'phone_number2', 'has_card',
            'has_key', 'skype', 'skills', 'assessment_date', 'assessment_plan', 'membershipmodel_set',
        ]
        read_only_fields = ['email', 'is_staff', 'has_card', 'has_key', 'assessment_date', 'assessment_plan']


class ApprovedByUserSerializer(DynamicFieldsMixin, ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'full_name']
        read_only_fields = ['email', 'full_name']

