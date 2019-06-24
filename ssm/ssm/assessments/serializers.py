from ssm.assessments.models import Assessment
from ssm.users.serializers import StaffUserDecisionBySerializer, StaffByUserSerializer, ByUserSerializer


CUSTOM_FIELDS = ['user', 'decision_by']
FIELDS = ['id', 'user', 'status', 'decision_by', 'start_date', 'end_date', 'plan', 'comments', 'notes']


class StaffAssessmentSerializer(StaffUserDecisionBySerializer):
    user = StaffByUserSerializer('user', required=False)
    decision_by = StaffByUserSerializer('decision_by', required=False, allow_null=True)

    class Meta:
        model = Assessment
        fields = FIELDS


class AssessmentSerializer(StaffAssessmentSerializer):
    user = ByUserSerializer('user', required=False, read_only=True)
    decision_by = ByUserSerializer('decision_by', required=False, read_only=True)

    class Meta(StaffAssessmentSerializer.Meta):
        read_only_fields = FIELDS
