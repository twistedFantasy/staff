from django.db import transaction

from rest_framework.serializers import Serializer, ModelSerializer, CharField, EmailField, IntegerField
from drf_writable_nested import WritableNestedModelSerializer

from ssm.users.models import User
from ssm.core.serializers import CustomTokenObtainPairSerializer
from ssm.core.helpers import cleanup


FIELDS = [
    'id', 'email', 'is_staff', 'full_name', 'date_of_birth', 'education', 'phone_number', 'phone_number2', 'has_card',
    'has_key', 'skype',
]
READ_ONLY_FIELDS = ['id', 'email', 'is_staff', 'has_card', 'has_key']


class SSMTokenObtainPairSerializer(CustomTokenObtainPairSerializer):
    pass


class ChangePasswordSerializer(Serializer):
    old_password = CharField(required=True)
    new_password = CharField(required=True)


class StaffByUserSerializer(ModelSerializer):
    id = IntegerField()
    email = EmailField(required=False)
    full_name = CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']


class ByUserSerializer(StaffByUserSerializer):

    class Meta(StaffByUserSerializer.Meta):
        read_only_fields = ['id', 'email', 'full_name']


class StaffUserSerializer(WritableNestedModelSerializer):
    email = EmailField(required=False)

    class Meta:
        model = User
        fields = FIELDS


class UserSerializer(StaffUserSerializer):

    class Meta(StaffUserSerializer.Meta):
        read_only_fields = READ_ONLY_FIELDS


class StaffUserWithSkillsSerializer(StaffUserSerializer):
    from ssm.skills.serializers import SkillOnlyAsNameSerializer
    skills = SkillOnlyAsNameSerializer(many=True, required=False)

    class Meta(StaffUserSerializer.Meta):
        fields = StaffUserSerializer.Meta.fields + ['skills']

    @transaction.atomic
    def update(self, instance, validated_data):
        from ssm.skills.models import Skill, UserSkillModel
        if 'skills' in validated_data:
            UserSkillModel.objects.filter(user=instance).delete()
            for skill in validated_data.pop('skills') or []:
                name = cleanup(skill['name'])
                skill = Skill.objects.filter(name=name).first()
                if not skill:
                    skill = Skill.objects.create(name=name)
                UserSkillModel(user=instance, skill=skill).save()

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class UserWithSkillsSerializer(StaffUserWithSkillsSerializer, UserSerializer):
    email = EmailField(required=False, read_only=True)

    class Meta(StaffUserWithSkillsSerializer.Meta):
        read_only_fields = READ_ONLY_FIELDS


class StaffUserDecisionBySerializer(ModelSerializer):

    def create(self, validated_data):
        self._transform(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._transform(validated_data)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    @staticmethod
    def _transform(data):
        if 'user' in data and (data['user'] or {}).get('id'):
            data['user'] = User.objects.get(id=data.pop('user')['id'])
        if 'decision_by' in data and (data['decision_by'] or {}).get('id'):
            data['decision_by'] = User.objects.get(id=data.pop('decision_by')['id'])
