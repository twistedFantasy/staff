from rest_framework.serializers import ModelSerializer

from ssm.assessments.models import Assessment
from ssm.users.serializers import ByUserSerializer


class StaffAssessmentSerializer(ModelSerializer):
    decision_by = ByUserSerializer('decision_by', read_only=True)

    class Meta:
        model = Assessment
        fields = ['id', 'user', 'status', 'decision_by', 'start_date', 'end_date', 'plan', 'comments']


class AssessmentSerializer(StaffAssessmentSerializer):

    class Meta(StaffAssessmentSerializer.Meta):
        read_only_fields = '__all__'
