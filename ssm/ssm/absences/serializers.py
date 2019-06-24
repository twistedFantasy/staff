from rest_framework.fields import DateField

from ssm.absences.models import Absence
from ssm.users.serializers import StaffUserDecisionBySerializer, StaffByUserSerializer, ByUserSerializer


FIELDS = ['id', 'reason', 'status', 'user', 'decision_by', 'start_date', 'end_date', 'notes']


class StaffAbsenceSerializer(StaffUserDecisionBySerializer):
    user = StaffByUserSerializer('user', required=False)
    decision_by = StaffByUserSerializer('decision_by', required=False, allow_null=True)
    start_date = DateField(required=False, allow_null=True)
    end_date = DateField(required=False, allow_null=True)

    class Meta:
        model = Absence
        fields = FIELDS


class AbsenceSerializer(StaffAbsenceSerializer):
    user = ByUserSerializer('user', required=False)
    decision_by = ByUserSerializer('decision_by', required=False, read_only=True)

    class Meta(StaffAbsenceSerializer.Meta):
        read_only_fields = ['id', 'decision_by', 'notes']
