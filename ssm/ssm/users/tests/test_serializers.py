import pytest

from django.test import TestCase
from django.db.utils import IntegrityError

from ssm.skills.models import Skill, UserSkillModel
from ssm.users.serializers import ChangePasswordSerializer, StaffUserWithSkillsSerializer, UserWithSkillsSerializer
from ssm.users.tests.factories import StaffUserFactory, UserFactory


class ChangePasswordSerializerTestCase(TestCase):

    def test_no_data(self):
        serializer = ChangePasswordSerializer(data={"old_password": "", "new_password": ""})
        assert not serializer.is_valid()

    def test_no_old_password(self):
        serializer = ChangePasswordSerializer(data={"old_password": "", "new_password": "new_password53"})
        assert not serializer.is_valid()

    def test_no_new_password(self):
        serializer = ChangePasswordSerializer(data={"old_password": "old_password53", "new_password": ""})
        assert not serializer.is_valid()

    def test_valid(self):
        serializer = ChangePasswordSerializer(
            data={"old_password": "old_password53", "new_password": "new_password53"}
        )
        assert serializer.is_valid()


class UserWithSkillsSerializerTestCase(TestCase):

    def setUp(self):
        self.staff_user = StaffUserFactory()
        self.simple_user = UserFactory()
        self.skill = Skill.objects.create(name='python')
        self.staff_user2 = StaffUserFactory()
        self.simple_user2 = UserFactory()
        UserSkillModel.objects.create(user=self.staff_user2, skill=self.skill)
        UserSkillModel.objects.create(user=self.simple_user2, skill=self.skill)

    def test_staff_serializer_with_skills__update__initial_empty_list_to_one_skill(self):
        serializer = StaffUserWithSkillsSerializer(self.staff_user)
        assert not serializer.data['skills']
        serializer = StaffUserWithSkillsSerializer(self.staff_user, data={'skills': [{'name': 'python'}]})
        assert serializer.is_valid()
        user = serializer.save()
        serializer = StaffUserWithSkillsSerializer(user)
        assert serializer.data['skills'] == [{'name': 'python'}]

    def test__staff_serializer_with_skills__update__initial_empty_list_to_three_skills(self):
        serializer = StaffUserWithSkillsSerializer(self.staff_user)
        assert not serializer.data['skills']
        data = {'skills': [{'name': 'postgresql'}, {'name': 'mysql'}]}
        serializer = StaffUserWithSkillsSerializer(self.staff_user, data=data)
        assert serializer.is_valid()
        user = serializer.save()
        serializer = StaffUserWithSkillsSerializer(user)
        assert len(serializer.data['skills']) == 2
        assert all(skill['name'] in ['postgresql', 'mysql'] for skill in serializer.data['skills'])

    def test__staff_serializer_with_skills__update__initial_one_skill_add_one_more_new(self):
        serializer = StaffUserWithSkillsSerializer(self.staff_user2)
        assert serializer.data['skills']
        data = {'skills': [{'name': 'python'}, {'name': 'golang'}]}
        serializer = StaffUserWithSkillsSerializer(self.staff_user2, data=data)
        assert serializer.is_valid()
        user = serializer.save()
        serializer = StaffUserWithSkillsSerializer(user)
        assert len(serializer.data['skills']) == 2
        assert all(skill['name'] in ['python', 'golang'] for skill in serializer.data['skills'])

    def test__staff_serializer_with_skills__update__initial_one_skill_add_one_more_but_the_same(self):
        serializer = StaffUserWithSkillsSerializer(self.staff_user2)
        assert serializer.data['skills']
        data = {'skills': [{'name': 'python'}, {'name': 'python'}]}
        serializer = StaffUserWithSkillsSerializer(self.staff_user2, data=data)
        assert serializer.is_valid()
        with pytest.raises(IntegrityError):
            serializer.save()

    def test_staff_serializer_with_skills__update__initial_one_skill_add_one_more_new_and_delete_previous(self):
        serializer = StaffUserWithSkillsSerializer(self.staff_user2)
        assert serializer.data['skills']
        serializer = StaffUserWithSkillsSerializer(self.staff_user2, data={'skills': [{'name': 'golang'}]})
        assert serializer.is_valid()
        user = serializer.save()
        serializer = StaffUserWithSkillsSerializer(user)
        assert len(serializer.data['skills']) == 1
        assert serializer.data['skills'][0]['name'] == 'golang'

    def test_staff_serializer_with_skills__update__initial_one_skill_add_one_more_with_wrong_format(self):
        serializer = StaffUserWithSkillsSerializer(self.staff_user2)
        assert serializer.data['skills']
        serializer = StaffUserWithSkillsSerializer(self.staff_user2, data={'skills': [{'nameZ': 'golang'}]})
        assert not serializer.is_valid()
        with pytest.raises(AssertionError):
            serializer.save()

    def test__staff_serializer_with_skills__update__initial_one_skill_remove_all_skills(self):
        serializer = StaffUserWithSkillsSerializer(self.staff_user2)
        assert serializer.data['skills']
        serializer = StaffUserWithSkillsSerializer(self.staff_user2, data={'skills': []})
        assert serializer.is_valid()
        user = serializer.save()
        serializer = StaffUserWithSkillsSerializer(user)
        assert not serializer.data['skills']

    def test_non_staff_serializer__read_only_fields(self):
        assert not self.simple_user.is_staff
        assert not self.simple_user.has_card
        assert not self.simple_user.has_key
        data = {'email': 'non-staff@gmail.com', 'is_staff': True, 'has_card': True, 'has_key': True}
        serializer = UserWithSkillsSerializer(self.simple_user, data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.email != data['email']
        assert not user.is_staff
        assert not user.has_card
        assert not user.has_key

    def test__non_staff_serializer_with_skills__update__initial_one_skill_add_one_more_new(self):
        serializer = UserWithSkillsSerializer(self.simple_user2)
        assert serializer.data['skills']
        data = {'skills': [{'name': 'python'}, {'name': 'golang'}]}
        serializer = UserWithSkillsSerializer(self.simple_user2, data=data)
        assert serializer.is_valid()
        user = serializer.save()
        serializer = UserWithSkillsSerializer(user)
        assert len(serializer.data['skills']) == 2
        assert all(skill['name'] in ['python', 'golang'] for skill in serializer.data['skills'])
