from django.test import TestCase

from ssm.assessments.tests.factories import AssessmentFactory


class AssessmentTestCase(TestCase):

    def test__str(self):
        assessment = AssessmentFactory()
        assert str(assessment) == f'{assessment.id} (assessment {assessment.user})'
