from django.urls import reverse
from rest_framework import status

from ssm.skills.models import Skill, UserSkillModel
from ssm.core.tests import BaseTestCase


class SkillTestCase(BaseTestCase):
    endpoint = 'skill-list'

    @classmethod
    def setUpTestData(cls):
        cls.skill1 = Skill.objects.create(name='python')
        cls.skill2 = Skill.objects.create(name='golang')
        Skill.objects.create(name='postgresql')
        Skill.objects.create(name='mysql')
        Skill.objects.create(name='mongodb')
        Skill.objects.create(name='aws')
        Skill.objects.create(name='gcloud')

    def setUp(self):
        super().setUp()
        UserSkillModel.objects.create(user=self.staff_user, skill=self.skill1)
        UserSkillModel.objects.create(user=self.simple_user, skill=self.skill1)

    def test_get_serializer_class__staff_without_users(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(reverse('skill-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 7
        assert all('users' not in value for value in response.data['results'])

    def test_get_serializer_class__staff_with_users(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(reverse('skill-list'), {'users': True})
        assert len(response.data['results']) == 7
        assert all('users' in value for value in response.data['results'])
        assert any(len(value['users']) == 2 for value in response.data['results'])

    def test_get_serializer_class__non_staff_without_users(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('skill-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert all('users' not in value for value in response.data['results'])

    def test_get_serializer_class__non_staff_with_users(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('skill-list'), {'users': True})
        assert len(response.data['results']) == 1
        assert all('users' in value for value in response.data['results'])
        assert all(len(value['users']) == 2 for value in response.data['results'])
        UserSkillModel.objects.create(user=self.simple_user, skill=self.skill2)
        response = self.client.get(reverse('skill-list'), {'users': True})
        assert len(response.data['results']) == 2
        assert all('users' in value for value in response.data['results'])
        assert all(len(value['users']) >= 1 for value in response.data['results'])
