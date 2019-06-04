from django.db import transaction

from rest_framework.serializers import ModelSerializer, CharField, EmailField, DateField
from drf_dynamic_fields import DynamicFieldsMixin
from drf_writable_nested import WritableNestedModelSerializer

from ssm.users.models import User, Absence, Assessment
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


class StaffAbsenceSerializer(DynamicFieldsMixin, ModelSerializer):
    user = StaffByUserSerializer('user', required=False)
    approved_by = StaffByUserSerializer('approved_by', required=False)
    start_date = DateField(required=False)
    end_date = DateField(required=False)

    class Meta:
        model = Absence
        fields = ['id', 'user', 'reason', 'status', 'approved_by', 'start_date', 'end_date', 'notes']


class AbsenceSerializer(StaffAbsenceSerializer):
    user = ByUserSerializer('user', required=False, read_only=True)
    approved_by = ByUserSerializer('approved_by', required=False, read_only=True)

    class Meta(StaffAbsenceSerializer.Meta):
        read_only_fields = ['id', 'user', 'approved_by']


class StaffAssessmentSerializer(ModelSerializer):
    decision_by = ByUserSerializer('decision_by', read_only=True)

    class Meta:
        model = Assessment
        fields = ['id', 'user', 'status', 'decision_by', 'start_date', 'end_date', 'plan', 'comments']


class AssessmentSerializer(StaffAssessmentSerializer):

    class Meta(StaffAssessmentSerializer.Meta):
        read_only_fields = '__all__'
