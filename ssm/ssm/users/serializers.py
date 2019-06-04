from django.db import transaction

from rest_framework.serializers import ModelSerializer, CharField, EmailField
from drf_dynamic_fields import DynamicFieldsMixin
from drf_writable_nested import WritableNestedModelSerializer

from ssm.users.models import User
from ssm.core.helpers import cleanup
from ssm.core.serializers import CustomTokenObtainPairSerializer


class SSMTokenObtainPairSerializer(CustomTokenObtainPairSerializer):
    pass


class StaffByUserSerializer(DynamicFieldsMixin, ModelSerializer):
    full_name = CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']


class ByUserSerializer(StaffByUserSerializer):

    class Meta(StaffByUserSerializer.Meta):
        read_only_fields = ['id', 'email', 'full_name']


class StaffUserWithSkillsSerializer(WritableNestedModelSerializer):
    from ssm.skills.serializers import SkillSerializer
    email = EmailField(required=False)
    skills = SkillSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'is_staff', 'full_name', 'date_of_birth', 'education', 'phone_number', 'phone_number2',
            'has_card', 'has_key', 'skype', 'skills',
        ]
        read_only_fields = []

    @transaction.atomic
    def update(self, instance, validated_data):
        from ssm.skills.models import Skill, UserSkillModel
        if 'skills' in validated_data:
            UserSkillModel.objects.filter(user=instance).delete()
            for data in validated_data.pop('skills') or []:
                name = cleanup(data['name'])
                skill = Skill.objects.filter(name=name).first()
                if not skill:
                    skill = Skill.objects.create(name=name)
                UserSkillModel(user=instance, skill=skill).save()

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class UserWithSkillsSerializer(StaffUserWithSkillsSerializer):
    email = EmailField(required=False, read_only=True)

    class Meta(StaffUserWithSkillsSerializer.Meta):
        read_only_fields = ['email', 'is_staff', 'has_card', 'has_key']
