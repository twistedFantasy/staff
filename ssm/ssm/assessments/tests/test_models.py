from django.test import TestCase

from ssm.assessments.tests.factories import AssessmentFactory, CheckpointFactory, TaskFactory


class AssessmentTestCase(TestCase):

    def test__str(self):
        assessment = AssessmentFactory()
        assert str(assessment) == f'{assessment.user} (assessment {assessment.id})'


class CheckpointTestCase(TestCase):

    def test__str(self):
        checkpoint = CheckpointFactory()
        assert str(checkpoint) == f'{checkpoint.date} (checkpoint {checkpoint.id})'


class TaskTestCase(TestCase):

    def test__str(self):
        task = TaskFactory()
        assert str(task) == f'{task.title} (task {task.id})'
