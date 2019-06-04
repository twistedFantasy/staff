import jwt
from django.conf import settings
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, \
    HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from ssm.users.serializers import StaffUserWithSkillsSerializer, UserWithSkillsSerializer
from ssm.core.tests import BaseTestCase


class SSMTokenObtainTestCase(BaseTestCase):

    def test_token_obtain__staff_user_correct_credentials(self):
        data = {'email': settings.TEST_STAFFUSER_EMAIL, 'password': settings.TEST_STAFFUSER_PASSWORD}
        token = self.client.post(reverse('auth'), data).data['token']
        assert len(token) > 100
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        assert decoded['token_type'] == 'access'
        assert decoded['user_id'] == self.staff_user.id
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        response = self.client.get(reverse('user-detail', args=[self.staff_user.id]), {'skills': True})
        assert response.status_code == HTTP_200_OK
        assert all([key in response.data for key in StaffUserWithSkillsSerializer.Meta.fields])

    def test_token_obtain__staff_user_incorrect_credentials_user_exist(self):
        data = {'email': settings.TEST_SIMPLEUSER_EMAIL, 'password': 'password'}
        response = self.client.post(reverse('auth'), data)
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_token_obtain__staff_user_incorrect_credentials_user_not_exist(self):
        data = {'email': 'test@gmail.com', 'password': 'password'}
        response = self.client.post(reverse('auth'), data)
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_token_obtain__simpleuser_correct_credentials(self):
        data = {'email': settings.TEST_SIMPLEUSER_EMAIL, 'password': settings.TEST_SIMPLEUSER_PASSWORD}
        token = self.client.post(reverse('auth'), data).data['token']
        assert len(token) > 100
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        assert decoded['token_type'] == 'access'
        assert decoded['user_id'] == self.simple_user.id
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        response = self.client.get(reverse('user-detail', args=[self.simple_user.id]), {'skills': True})
        assert response.status_code == HTTP_200_OK
        assert all([key in response.data for key in UserWithSkillsSerializer.Meta.fields])


class UserViewSetTestCase(BaseTestCase):
    endpoint = 'user-list'

    @classmethod
    def setUpTestData(cls):
        from ssm.skills.models import Skill
        cls.skill1 = Skill.objects.create(name='python')
        cls.skill2 = Skill.objects.create(name='golang')
        Skill.objects.create(name='postgresql')
        Skill.objects.create(name='mysql')
        Skill.objects.create(name='mongodb')
        Skill.objects.create(name='aws')
        Skill.objects.create(name='gcloud')

    def test_permission_classes__staff_allow_to_use_any_rest_method(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(reverse('user-list'))
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        response = self.client.get(reverse('user-detail', args=[self.staff_user.id]))
        assert response.status_code == HTTP_200_OK
        assert response.data['email'] == self.staff_user.email
        response = self.client.patch(reverse('user-detail', args=[self.staff_user.id]), data={'skype': 'test'})
        assert response.status_code == HTTP_200_OK
        assert response.data['skype'] == 'test'
        data = {'email': 'UserViewSetTestCase@gmail.com', 'password': 'password', 'skills': []}
        response = self.client.post(reverse('user-list'), data=data)
        assert response.status_code == HTTP_201_CREATED
        assert response.data['email'] == data['email']
        response = self.client.delete(reverse('user-detail', args=[response.data['id']]))
        assert response.status_code == HTTP_204_NO_CONTENT

    def test_permission_classes__non_staff_allow_to_use_subset_of_rest_api_methods(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('user-list'))
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 1
        response = self.client.get(reverse('user-detail', args=[self.simple_user.id]))
        assert response.status_code == HTTP_200_OK
        assert response.data['email'] == self.simple_user.email
        response = self.client.patch(reverse('user-detail', args=[self.simple_user.id]), data={'skype': 'test'})
        assert response.status_code == HTTP_200_OK
        assert response.data['skype'] == 'test'
        data = {'email': 'UserViewSetTestCase@gmail.com', 'password': 'password', 'skills': []}
        response = self.client.post(reverse('user-list'), data=data)
        assert response.status_code == HTTP_403_FORBIDDEN
        response = self.client.delete(reverse('user-detail', args=[self.simple_user.id]))
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_permission_classes__staff_allows_to_access_and_modify_any_other_users_data(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(reverse('user-list'))
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        response = self.client.get(reverse('user-detail', args=[self.simple_user.id]))
        assert response.status_code == HTTP_200_OK
        assert response.data['email'] == self.simple_user.email
        response = self.client.patch(reverse('user-detail', args=[self.simple_user.id]), data={'skype': 'test'})
        assert response.status_code == HTTP_200_OK
        assert response.data['skype'] == 'test'
        data = {'email': 'UserViewSetTestCase@gmail.com', 'password': 'password', 'skills': []}
        response = self.client.post(reverse('user-list'), data=data)
        assert response.status_code == HTTP_201_CREATED
        assert response.data['email'] == data['email']
        response = self.client.delete(reverse('user-detail', args=[response.data['id']]))
        assert response.status_code == HTTP_204_NO_CONTENT

    def test_permission_classes__non_staff_allows_to_access_and_modify_only_his_data(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('user-list'))
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 1
        response = self.client.get(reverse('user-detail', args=[self.simple_user.id]))
        assert response.status_code == HTTP_200_OK
        assert response.data['email'] == self.simple_user.email
        response = self.client.get(reverse('user-detail', args=[self.staff_user.id]))
        assert response.status_code == HTTP_404_NOT_FOUND
        response = self.client.patch(reverse('user-detail', args=[self.staff_user.id]), data={'skype': 'test'})
        assert response.status_code == HTTP_404_NOT_FOUND
        data = {'email': 'UserViewSetTestCase@gmail.com', 'password': 'password', 'skills': []}
        response = self.client.post(reverse('user-list'), data=data)
        assert response.status_code == HTTP_403_FORBIDDEN
        response = self.client.delete(reverse('user-detail', args=[self.staff_user.id]))
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_get_serializer_class__staff_user_allow_to_modify_all_fields(self):
        data = {'email': 'staff.new@gmail.com', 'is_staff': True, 'has_card': True, 'has_key': True}
        assert self.simple_user.email != data['email']
        assert not self.simple_user.is_staff
        assert not self.simple_user.has_card
        assert not self.simple_user.has_key
        self.client.force_authenticate(self.staff_user)
        response = self.client.patch(reverse('user-detail', args=[self.staff_user.id]), data)
        assert response.data['email'] == data['email']
        assert response.data['is_staff']
        assert response.data['has_card']
        assert response.data['has_key']

    def test_get_serializer_class_non_staff_user_allow_to_modify_non_read_only_fields(self):
        data = {'email': 'non-staf.new@gmail.com', 'is_staff': True, 'has_card': True, 'has_key': True}
        assert self.simple_user.email != data['email']
        assert not self.simple_user.is_staff
        assert not self.simple_user.has_card
        assert not self.simple_user.has_key
        self.client.force_authenticate(self.simple_user)
        response = self.client.patch(reverse('user-detail', args=[self.simple_user.id]), data)
        assert response.data['email'] != data['email']
        assert not response.data['is_staff']
        assert not response.data['has_card']
        assert not response.data['has_key']

    def test_get_serializer_class__staff_without_skills(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(reverse('user-list'))
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        assert all('skills' not in value for value in response.data['results'])

    def test_get_serializer_class__staff_with_skills(self):
        from ssm.skills.models import UserSkillModel
        UserSkillModel.objects.create(user=self.staff_user, skill=self.skill1)
        UserSkillModel.objects.create(user=self.simple_user, skill=self.skill2)
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(reverse('user-list'), {'skills': True})
        assert len(response.data['results']) == 2
        assert all('skills' in value for value in response.data['results'])
        assert all(len(value['skills']) == 1 for value in response.data['results'])

    def test_get_serializer_class__non_staff_without_users(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('user-list'))
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 1
        assert all('skills' not in value for value in response.data['results'])

    def test_get_serializer_class__non_staff_with_users(self):
        from ssm.skills.models import UserSkillModel
        UserSkillModel.objects.create(user=self.simple_user, skill=self.skill1)
        UserSkillModel.objects.create(user=self.simple_user, skill=self.skill2)
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('user-list'), {'skills': True})
        assert len(response.data['results']) == 1
        assert all('skills' in value for value in response.data['results'])
        assert all(len(value['skills']) == 2 for value in response.data['results'])


class ChangePasswordTestCase(BaseTestCase):

    def test_permission_classes__only_is_authenticated_user_allows_access(self):
        data = {'password': 'new_password'}
        response = self.client.patch(reverse('change_password'), data)
        assert response.status_code == HTTP_401_UNAUTHORIZED
        self.client.force_authenticate(self.simple_user)
        response = self.client.patch(reverse('change_password'), data)
        assert response.status_code == HTTP_200_OK
        self.client.force_authenticate()
        token = self.client.post(reverse('auth'), {**{'email': self.simple_user.email}, **data}).data['token']
        assert len(token) > 100
