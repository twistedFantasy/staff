from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from ssm.projects.models import Project, MembersModel
from ssm.core.tests import BaseTestCase
from ssm.core.helpers import today


class ProjectTestCase(BaseTestCase):
    endpoint = 'project-list'

    @classmethod
    def setUpTestData(cls):
        cls.project1 = Project.objects.create(name='Project1')
        cls.project2 = Project.objects.create(name='Project2')

    def setUp(self):
        super().setUp()
        MembersModel.objects.create(user=self.staff_user, project=self.project1, joined_date=today())
        MembersModel.objects.create(user=self.simple_user, project=self.project1, joined_date=today())
        MembersModel.objects.create(user=self.simple_user, project=self.project2, joined_date=today())

    def test_get_serializer_class__staff__request__projects_without_members(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(reverse('project-list'))
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        assert all('members' not in value for value in response.data['results'])

    def test_get_serializer_class__staff_request__projects__with_members(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(reverse('project-list'), {'members': True})
        assert len(response.data['results']) == 2
        assert all('members' in value for value in response.data['results'])
        assert any(len(value['members']) == 2 for value in response.data['results'])

    def test_get_serializer_class__non_staff_request__projects_without_members(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('project-list'))
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        assert all('members' not in value for value in response.data['results'])

    def test_get_serializer_class__non_staff_request__projects_with_members(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('project-list'), {'members': True})
        assert len(response.data['results']) == 2
        assert all('members' in value for value in response.data['results'])
        assert all(len(value['members']) >= 1 for value in response.data['results'])
