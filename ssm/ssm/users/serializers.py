from django.db import transaction

from rest_framework.serializers import ModelSerializer
from drf_dynamic_fields import DynamicFieldsMixin
from drf_writable_nested import WritableNestedModelSerializer

from ssm.users.models import User
from ssm.core.serializers import CustomTokenObtainPairSerializer


class SSMTokenObtainPairSerializer(CustomTokenObtainPairSerializer):
    pass


class UserSerializer(DynamicFieldsMixin, ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'email', 'is_staff', 'full_name', 'date_of_birth', 'education', 'phone_number', 'phone_number2',
            'has_card', 'has_key', 'skype', 'assessment_date', 'assessment_plan',
        ]
        read_only_fields = ['id', 'email', 'is_staff', 'has_card', 'has_key', 'assessment_date', 'assessment_plan']


class UserWithSkillsSerializer(UserSerializer, WritableNestedModelSerializer):
    from ssm.skills.serializers import SkillSerializer
    skills = SkillSerializer(many=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['skills']

    @transaction.atomic
    def update(self, instance, validated_data):
        from ssm.skills.models import Skill, UserSkillModel
        if 'skills' in validated_data:
            UserSkillModel.objects.filter(user=instance).delete()
            for data in validated_data.pop('skills') or []:
                name = data['name'].lower().strip()
                skill = Skill.objects.filter(name=name).first()
                if not skill:
                    skill = Skill.objects.create(name=name)
                UserSkillModel(user=instance, skill=skill).save()

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class ApprovedByUserSerializer(DynamicFieldsMixin, ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'full_name']
        read_only_fields = ['email', 'full_name']
