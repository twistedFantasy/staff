from rest_framework.serializers import ModelSerializer

from ssm.assessments.models import Assessment, Checkpoint, Task
from ssm.users.serializers import StaffUserDecisionBySerializer, StaffByUserSerializer, ByUserSerializer


ASSESSMENT_CUSTOM_FIELDS = ['user', 'decision_by']
ASSESSMENT_FIELDS = ['id', 'user', 'status', 'decision_by', 'start_date', 'end_date', 'plan', 'comments', 'notes']
CHECKPOINT_FIELDS = ['id', 'assessment', 'title', 'date']
TASK_FIELDS = ['id', 'checkpoint', 'title', 'description', 'completed']


class StaffAssessmentSerializer(StaffUserDecisionBySerializer):
    user = StaffByUserSerializer('user', required=False)
    decision_by = StaffByUserSerializer('decision_by', required=False, allow_null=True)

    class Meta:
        model = Assessment
        fields = ASSESSMENT_FIELDS


class AssessmentSerializer(StaffAssessmentSerializer):
    user = ByUserSerializer('user', required=False, read_only=True)
    decision_by = ByUserSerializer('decision_by', required=False, read_only=True)

    class Meta(StaffAssessmentSerializer.Meta):
        read_only_fields = ASSESSMENT_FIELDS


class StaffCheckpointSerializer(ModelSerializer):

    class Meta:
        model = Checkpoint
        fields = CHECKPOINT_FIELDS


class CheckpointSerializer(StaffCheckpointSerializer):

    class Meta(StaffCheckpointSerializer.Meta):
        read_only_fields = CHECKPOINT_FIELDS


class StaffTaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = TASK_FIELDS


class TaskSerializer(StaffTaskSerializer):

    class Meta(StaffTaskSerializer.Meta):
        read_only_fields = TASK_FIELDS
