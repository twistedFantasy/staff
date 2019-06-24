import jwt
from django.conf import settings
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, \
    HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from ssm.users.models import User
from ssm.users.serializers import StaffUserWithSkillsSerializer, UserWithSkillsSerializer
from ssm.users.tests.factories import StaffUserFactory, UserFactory
from ssm.core.tests import BaseTestCase


class UserViewSetTestCase(BaseTestCase):
    list_url = 'user-list'
    detail_url = 'user-detail'

    def setUp(self):
        # self.list_url = reverse('company-list')
        self.staff_user = StaffUserFactory()
        self.simple_user = UserFactory()
        from ssm.skills.models import Skill
        self.skill1 = Skill.objects.create(name='python')
        self.skill2 = Skill.objects.create(name='golang')
        Skill.objects.create(name='postgresql')
        Skill.objects.create(name='mysql')
        Skill.objects.create(name='mongodb')
        Skill.objects.create(name='aws')
        Skill.objects.create(name='gcloud')

    def test_permission_classes__only_is_authenticated_user_allows_access(self):
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_401_UNAUTHORIZED
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_permission_classes__staff_allow_to_use_any_rest_method(self):
        self.client.force_authenticate(self.staff_user)

        # POST
        assert User.objects.count() == 2
        data = {'email': self.fake.email(), 'password': self.fake.password(), 'skills': []}
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_201_CREATED
        assert User.objects.count() == 3
        user = User.objects.get(email=data['email'])
        self.assert_fields(user, data, self.staff_user)

        # GET(id)
        response = self.client.get(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_200_OK
        assert response.data['email'] == data['email']
        serializer = StaffUserWithSkillsSerializer(user)
        assert response.data == serializer.data

        # PATCH
        data = {'skype': self.fake.user_name()}
        response = self.client.patch(self.get_detail_url(response.data['id']), data=data)
        user.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['skype'] == data['skype']
        assert user.skype == data['skype']

        # PUT
        data = {**response.data, **{'skype': self.fake.user_name()}}
        response = self.client.put(self.get_detail_url(response.data['id']), data=data)
        user.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['skype'] == data['skype']
        assert user.skype == data['skype']

        # DELETE
        assert User.objects.count() == 3
        response = self.client.delete(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_204_NO_CONTENT
        assert User.objects.count() == 2

        # GET(all)
        [UserFactory(email=email) for email in [self.fake.email, self.fake.email()]]
        users = User.objects.all()
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 4
        serializer = StaffUserWithSkillsSerializer(users, many=True)
        assert response.data['results'] == serializer.data
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in users)

    def test_permission_classes__non_staff_allow_to_use_subset_of_rest_api_methods(self):
        self.client.force_authenticate(self.simple_user)

        # POST
        assert User.objects.count() == 2
        data = {'email': self.fake.email(), 'password': self.fake.password(), 'skills': []}
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_403_FORBIDDEN
        assert User.objects.count() == 2

        # GET(id)
        response = self.client.get(self.get_detail_url(self.simple_user.id))
        assert response.status_code == HTTP_200_OK
        serializer = UserWithSkillsSerializer(self.simple_user)
        assert response.data == serializer.data

        # PATCH
        data = {'skype': self.fake.user_name()}
        response = self.client.patch(self.get_detail_url(self.simple_user.id), data=data)
        self.simple_user.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['skype'] == data['skype']
        assert self.simple_user.skype == data['skype']

        # PUT
        data = {**response.data, **{'skype': self.fake.user_name()}}
        response = self.client.put(self.get_detail_url(self.simple_user.id), data=data)
        self.simple_user.refresh_from_db()
        assert response.status_code == HTTP_403_FORBIDDEN
        assert self.simple_user.skype != data['skype']

        # DELETE
        response = self.client.delete(self.get_detail_url(self.simple_user.id))
        assert response.status_code == HTTP_403_FORBIDDEN
        assert User.objects.count() == 2

        # GET(all)
        [UserFactory(email=email) for email in [self.fake.email(), self.fake.email()]]
        users = User.objects.filter(email=self.simple_user.email)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 1
        serializer = UserWithSkillsSerializer(users, many=True)
        assert response.data['results'] == serializer.data
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in users)

    def test_permission_classes__staff_allows_to_access_and_modify_any_other_users_data(self):
        self.client.force_authenticate(self.staff_user)

        # POST
        assert User.objects.count() == 2
        data = {'email': self.fake.email(), 'password': self.fake.password(), 'skills': []}
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_201_CREATED
        assert response.data['email'] == data['email']
        user = User.objects.get(email=data['email'])
        self.assert_fields(user, data, self.simple_user)

        # GET(id)
        response = self.client.get(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_200_OK
        serializer = StaffUserWithSkillsSerializer(user)
        assert response.data == serializer.data

        # PATCH
        data = {'skype': self.fake.user_name()}
        response = self.client.patch(self.get_detail_url(response.data['id']), data=data)
        user.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['skype'] == data['skype']
        assert user.skype == data['skype']

        # PUT
        data = {**response.data, **{'skype': self.fake.user_name()}}
        response = self.client.put(self.get_detail_url(response.data['id']), data=data)
        user.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['skype'] == data['skype']
        assert user.skype == data['skype']

        # DELETE
        assert User.objects.count() == 3
        response = self.client.delete(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_204_NO_CONTENT
        assert User.objects.count() == 2

        # GET(all)
        [UserFactory(email=email) for email in [self.fake.email(), self.fake.email()]]
        users = User.objects.all()
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 4
        serializer = StaffUserWithSkillsSerializer(users, many=True)
        assert response.data['results'] == serializer.data
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in users)

    def test_permission_classes__non_staff_allows_to_access_and_modify_only_his_data(self):
        self.client.force_authenticate(self.simple_user)

        # POST
        assert User.objects.count() == 2
        data = {'email': self.fake.email(), 'password': self.fake.password(), 'skills': []}
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_403_FORBIDDEN
        assert User.objects.count() == 2

        # GET(id)
        response = self.client.get(self.get_detail_url(self.staff_user.id))
        assert response.status_code == HTTP_404_NOT_FOUND

        # PATCH
        data = {'skype': self.fake.user_name()}
        response = self.client.patch(self.get_detail_url(self.staff_user.id), data=data)
        assert response.status_code == HTTP_404_NOT_FOUND

        # DELETE
        response = self.client.delete(self.get_detail_url(self.staff_user.id))
        assert response.status_code == HTTP_403_FORBIDDEN

        # GET(all)
        [UserFactory(email=email) for email in [self.fake.email(), self.fake.email()]]
        users = User.objects.filter(email=self.simple_user.email)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 1
        assert User.objects.count() == 4
        serializer = UserWithSkillsSerializer(users, many=True)
        assert response.data['results'] == serializer.data

    def test_get_serializer_class__staff_absence_serializer(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.get_detail_url(self.staff_user.id))
        serializer = StaffUserWithSkillsSerializer(self.staff_user)
        assert response.status_code == HTTP_200_OK
        assert response.data == serializer.data

    def test_get_serializer_class__absence_serializer(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(self.get_detail_url(self.simple_user.id))
        serializer = UserWithSkillsSerializer(self.simple_user)
        assert response.status_code == HTTP_200_OK
        assert response.data == serializer.data

    def test_get_serializer_class__staff_user_allow_to_modify_all_fields(self):
        user = UserFactory()
        self.client.force_authenticate(self.staff_user)
        data = {'email': 'staff.new@gmail.com', 'is_staff': True, 'has_card': True, 'has_key': True}
        response = self.client.patch(self.get_detail_url(user.id), data=data)
        user.refresh_from_db()
        for field in data.keys():
            assert response.data[field] == data[field]
            assert getattr(user, field) == data[field]

    def test_get_serializer_class__non_staff_user_allow_to_modify_non_read_only_fields(self):
        self.client.force_authenticate(self.simple_user)
        data = {'email': 'staff.new@gmail.com', 'is_staff': True, 'has_card': True, 'has_key': True}
        response = self.client.patch(self.get_detail_url(self.simple_user.id), data=data)
        assert response.status_code == HTTP_200_OK
        self.simple_user.refresh_from_db()
        for field in data.keys():
            assert getattr(self.simple_user, field) != data[field]
        data = {
            'full_name': self.fake.name(),
            'date_of_birth': self.fake.date_of_birth(),
            'education': self.fake.hostname(),
            'phone_number': self.fake.phone_number(),
            'phone_number2': self.fake.phone_number(),
            'skype': self.fake.user_name(),
        }
        response = self.client.patch(self.get_detail_url(self.simple_user.id), data=data)
        assert response.status_code == HTTP_200_OK
        self.simple_user.refresh_from_db()
        for field in data.keys():
            assert getattr(self.simple_user, field) == data[field]

    def test_get_serializer_class__staff_request__without_skills(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.get_list_url(), {'skills': False})
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        assert all('skills' not in value for value in response.data['results'])
        response = self.client.get(self.get_list_url(), {'skills': 'false'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        assert all('skills' not in value for value in response.data['results'])
        response = self.client.get(self.get_list_url(), {'skills': 0})
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        assert all('skills' not in value for value in response.data['results'])

    def test_get_serializer_class__staff_request__with_skills(self):
        from ssm.skills.models import UserSkillModel
        UserSkillModel.objects.create(user=self.staff_user, skill=self.skill1)
        UserSkillModel.objects.create(user=self.simple_user, skill=self.skill2)
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.get_list_url())
        assert len(response.data['results']) == 2
        assert all('skills' in value for value in response.data['results'])
        assert any(len(value['skills']) == 1 for value in response.data['results'])
        response = self.client.get(self.get_list_url(), {'skills': True})
        assert len(response.data['results']) == 2
        assert all('skills' in value for value in response.data['results'])
        assert any(len(value['skills']) == 1 for value in response.data['results'])

    def test_get_serializer_class__non_staff_request__without_skills(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(self.get_list_url(),  {'skills': False})
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 1
        assert all('skills' not in value for value in response.data['results'])
        response = self.client.get(self.get_list_url(), {'skills': 'false'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 1
        assert all('skills' not in value for value in response.data['results'])
        response = self.client.get(self.get_list_url(), {'skills': 0})
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 1
        assert all('skills' not in value for value in response.data['results'])

    def test_get_serializer_class__non_staff_request__with_skills(self):
        from ssm.skills.models import UserSkillModel
        UserSkillModel.objects.create(user=self.simple_user, skill=self.skill1)
        UserSkillModel.objects.create(user=self.simple_user, skill=self.skill2)
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(self.get_list_url())
        assert len(response.data['results']) == 1
        assert all('skills' in value for value in response.data['results'])
        assert all(len(value['skills']) == 2 for value in response.data['results'])
        response = self.client.get(self.get_list_url(), {'skills': True})
        assert len(response.data['results']) == 1
        assert all('skills' in value for value in response.data['results'])
        assert all(len(value['skills']) == 2 for value in response.data['results'])


class SSMTokenObtainTestCase(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        data = {'email': settings.TEST_STAFFUSER_EMAIL, 'password': settings.TEST_STAFFUSER_PASSWORD}
        cls.staff_user = User.objects.create_superuser(**data)
        data = {'email': settings.TEST_SIMPLEUSER_EMAIL, 'password': settings.TEST_SIMPLEUSER_PASSWORD}
        cls.simple_user = User.objects.create_user(**data)

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


class ChangePasswordTestCase(BaseTestCase):

    def test_permission_classes__only_is_authenticated_user_allows_access(self):
        simple_user = UserFactory()
        data = {'password': self.fake.password()}
        response = self.client.patch(reverse('change_password'), data)
        assert response.status_code == HTTP_401_UNAUTHORIZED
        self.client.force_authenticate(simple_user)
        response = self.client.patch(reverse('change_password'), data)
        assert response.status_code == HTTP_200_OK
        self.client.force_authenticate()
        token = self.client.post(reverse('auth'), {**{'email': simple_user.email}, **data}).data['token']
        assert len(token) > 100
