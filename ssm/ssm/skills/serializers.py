from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework.serializers import ModelSerializer

from ssm.skills.models import Skill


class SkillOnlyAsNameSerializer(DynamicFieldsMixin, ModelSerializer):

    class Meta:
        model = Skill
        fields = ['name']
        extra_kwargs = {'name': {'validators': []}}


class StaffSkillSerializer(ModelSerializer):

    class Meta:
        model = Skill
        fields = '__all__'


class SkillSerializer(StaffSkillSerializer):

    class Meta(StaffSkillSerializer.Meta):
        read_only_fields = ['name', 'category']


class StaffSkillWithUsersSerializer(StaffSkillSerializer):
    from ssm.users.serializers import StaffByUserSerializer
    users = StaffByUserSerializer(source='user_set', many=True)

    class Meta(StaffSkillSerializer.Meta):
        pass


class SkillWithUsersSerializer(SkillSerializer):
    from ssm.users.serializers import ByUserSerializer
    users = ByUserSerializer(source='user_set', many=True, read_only=True)

    class Meta(SkillSerializer.Meta):
        read_only_fields = SkillSerializer.Meta.read_only_fields + ['users']
