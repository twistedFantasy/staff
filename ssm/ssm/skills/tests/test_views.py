from django.urls import reverse
from rest_framework import status

from ssm.skills.models import Skill
from ssm.core.tests import BaseTestCase


class SkillTestCase(BaseTestCase):

    def test_skill__get_by_id(self):
        Skill.objects.create(name='python')
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(reverse('skill-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0] == {'name': 'python', 'users': []}
