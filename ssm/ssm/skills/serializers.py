from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework.serializers import ModelSerializer

from ssm.skills.models import Skill


class SkillSerializer(DynamicFieldsMixin, ModelSerializer):

    class Meta:
        model = Skill
        fields = ['name']
        read_only_fields = ['name']
