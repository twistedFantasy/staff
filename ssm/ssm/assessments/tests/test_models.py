from django.test import TestCase

from ssm.assessments.tests.factories import AssessmentFactory, CheckpointFactory, TaskFactory


class AssessmentTestCase(TestCase):

    def test__str(self):
        assessment = AssessmentFactory()
        assert str(assessment) == f'{assessment.id} (assessment {assessment.user})'


class CheckpointTestCase(TestCase):

    def test__str(self):
        checkpoint = CheckpointFactory()
        assert str(checkpoint) == f'{checkpoint.id} (checkpoint {checkpoint.date})'


class TaskTestCase(TestCase):

    def test__str(self):
        task = TaskFactory()
        assert str(task) == f'{task.title} (task {task.id})'
