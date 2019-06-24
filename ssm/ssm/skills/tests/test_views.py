from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from ssm.skills.models import UserSkillModel
from ssm.skills.tests.factories import SkillFactory
from ssm.users.tests.factories import StaffUserFactory, UserFactory
from ssm.core.tests import BaseTestCase


class SkillTestCase(BaseTestCase):
    list_url = 'skill-list'
    detail_url = 'skill-detail'

    @classmethod
    def setUpTestData(cls):
        cls.skill1 = SkillFactory(name='python')
        cls.skill2 = SkillFactory(name='golang')
        [SkillFactory(name=name) for name in ['postgresql', 'mysql', 'mongodb', 'aws', 'gcloud']]

    def setUp(self):
        self.staff_user = StaffUserFactory()
        self.simple_user = UserFactory()
        UserSkillModel.objects.create(user=self.staff_user, skill=self.skill1)
        UserSkillModel.objects.create(user=self.simple_user, skill=self.skill1)

    def test_permission_classes__only_is_authenticated_user_allows_access(self):
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_401_UNAUTHORIZED
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 7

    def test_get_serializer_class__staff_request__skills_without_users(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 7
        assert all('users' not in value for value in response.data['results'])

    def test_get_serializer_class__staff_request__skills_with_users(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.get_list_url(), {'users': True})
        assert len(response.data['results']) == 7
        assert all('users' in value for value in response.data['results'])
        assert any(len(value['users']) == 2 for value in response.data['results'])

    def test_get_serializer_class__non_staff_request__skills_without_users(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 1
        assert all('users' not in value for value in response.data['results'])

    def test_get_serializer_class__non_staff_request__skills_with_users(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(self.get_list_url(), {'users': True})
        assert len(response.data['results']) == 1
        assert all('users' in value for value in response.data['results'])
        assert all(len(value['users']) == 2 for value in response.data['results'])
        UserSkillModel.objects.create(user=self.simple_user, skill=self.skill2)
        response = self.client.get(self.get_list_url(), {'users': True})
        assert len(response.data['results']) == 2
        assert all('users' in value for value in response.data['results'])
        assert all(len(value['users']) >= 1 for value in response.data['results'])
