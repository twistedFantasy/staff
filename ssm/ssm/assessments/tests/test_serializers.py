from django.test import TestCase

from ssm.assessments.models import STATUS
from ssm.assessments.tests.factories import AssessmentFactory
from ssm.assessments.serializers import StaffAssessmentSerializer, AssessmentSerializer, ASSESSMENT_FIELDS, \
    ASSESSMENT_CUSTOM_FIELDS
from ssm.users.tests.factories import UserFactory
from ssm.core.helpers import Day


class StaffAssessmentSerializerTestCase(TestCase):

    def test__model_fields(self):
        assessment = AssessmentFactory()
        serializer = StaffAssessmentSerializer(assessment)
        for field in ASSESSMENT_FIELDS:
            if field not in ['user', 'decision_by']:
                assert serializer.data[field] == getattr(assessment, field)

    def test__empty_read_only_fields(self):
        assessment = AssessmentFactory(status=STATUS.new, start_date=Day().date, end_date=Day().date)
        user, decision_by = UserFactory(), UserFactory()
        data = {
            'user': {'id': user.id},
            'decision_by': {'id': decision_by.id},
            'status': STATUS.in_progress,
            'start_date': Day(ago=5).date,
            'end_date': Day(ago=5).date,
            'plan': 'Test plan',
            'comments': 'Test comments',
            'notes': 'Test notes',
        }
        serializer = StaffAssessmentSerializer(assessment, data=data)
        assert serializer.is_valid()
        assessment = serializer.save()
        assert assessment.user.id == data['user']['id']
        assert assessment.decision_by.id == data['decision_by']['id']
        data.pop('user'), data.pop('decision_by')
        for field in data.keys():
            assert getattr(assessment, field) == data[field]


class AssessmentSerializerTestCase(TestCase):

    def test__read_only_fields(self):
        assessment = AssessmentFactory(status=STATUS.new, start_date=Day().date, end_date=Day().date)
        user, decision_by = UserFactory(), UserFactory()
        data = {
            'user': {'id': user.id},
            'decision_by': {'id': decision_by.id},
            'status': STATUS.in_progress,
            'start_date': Day(ago=5).date,
            'end_date': Day(ago=5).date,
            'plan': 'Test plan',
            'comments': 'Test comments',
            'notes': 'Test notes',
        }
        serializer = AssessmentSerializer(assessment, data=data)
        assert serializer.is_valid()
        assessment = serializer.save()
        assert assessment.user.id != data['user']['id']
        assert assessment.decision_by.id != data['user']['id']
        data.pop('user'), data.pop('decision_by')
        for field in data.keys():
            assert getattr(assessment, field) != data[field]
