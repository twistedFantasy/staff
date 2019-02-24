from rest_framework.serializers import ModelSerializer
from drf_dynamic_fields import DynamicFieldsMixin

from ssm.absences.models import Absence
from ssm.users.serializers import ApprovedByUserSerializer


class AbsenceSerializer(DynamicFieldsMixin, ModelSerializer):
    approved_by = ApprovedByUserSerializer('approved_by', read_only=True)

    class Meta:
        model = Absence
        fields = ['id', 'user', 'reason', 'status', 'approved_by', 'start_date', 'end_date', 'notes']
        read_only_fields = ['id', 'user', 'approved_by']
