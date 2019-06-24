from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework.serializers import ModelSerializer

from ssm.skills.models import Skill


SKILL_FIELDS = ['id', 'name', 'category']


class SkillOnlyAsNameSerializer(DynamicFieldsMixin, ModelSerializer):

    class Meta:
        model = Skill
        fields = ['name']
        extra_kwargs = {'name': {'validators': []}}


class StaffSkillSerializer(ModelSerializer):

    class Meta:
        model = Skill
        fields = SKILL_FIELDS


class SkillSerializer(StaffSkillSerializer):

    class Meta(StaffSkillSerializer.Meta):
        read_only_fields = SKILL_FIELDS


class StaffSkillWithUsersSerializer(StaffSkillSerializer):
    from ssm.users.serializers import StaffByUserSerializer
    users = StaffByUserSerializer(source='user_set', many=True)

    class Meta(StaffSkillSerializer.Meta):
        fields = StaffSkillSerializer.Meta.fields + ['users']


class SkillWithUsersSerializer(SkillSerializer):
    from ssm.users.serializers import ByUserSerializer
    users = ByUserSerializer(source='user_set', many=True, read_only=True)

    class Meta(SkillSerializer.Meta):
        fields = SkillSerializer.Meta.fields + ['users']
        read_only_fields = SkillSerializer.Meta.read_only_fields + ['users']
