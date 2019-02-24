from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework.serializers import ModelSerializer

from ssm.skills.models import Skill


class SkillSerializer(DynamicFieldsMixin, ModelSerializer):

    class Meta:
        model = Skill
        fields = ['name']
        extra_kwargs = {'name': {'validators': []}}


class SkillWithUsersSerializer(SkillSerializer):
    from ssm.users.serializers import UserSerializer
    users = UserSerializer(source='user_set', many=True, read_only=True)

    class Meta(SkillSerializer.Meta):
        fields = SkillSerializer.Meta.fields + ['users']
