from rest_framework.serializers import ModelSerializer, DateField
from drf_dynamic_fields import DynamicFieldsMixin

from ssm.absences.models import Absence
from ssm.users.serializers import StaffByUserSerializer, ByUserSerializer


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
