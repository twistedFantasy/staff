from django.test import TestCase

from ssm.projects.tests.factories import ProjectFactory


class ProjectTestCase(TestCase):

    def test__str(self):
        project = ProjectFactory()
        assert str(project) == f'{project.name} (project {project.id})'
