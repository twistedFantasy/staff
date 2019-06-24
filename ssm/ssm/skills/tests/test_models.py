from django.test import TestCase
from ssm.skills.models import CATEGORY
from ssm.skills.tests.factories import SkillFactory


class SkillTestCase(TestCase):

    def test_str(self):
        skill = SkillFactory()
        assert str(skill) == f'{skill.name} (skill {skill.id})'

    def test_name_field_should_be_lowercase(self):
        skill = SkillFactory(name='PYTHON', category=CATEGORY.programming_language)
        assert skill.name == 'python'
        skill = SkillFactory(name='PostgreSQL', category=CATEGORY.database)
        assert skill.name == 'postgresql'
        skill = SkillFactory(name='golang', category=CATEGORY.programming_language)
        assert skill.name == 'golang'
        skill = SkillFactory(name=' mongodb', category=CATEGORY.database)
        assert skill.name == 'mongodb'
        skill = SkillFactory(name='mysql ', category=CATEGORY.database)
        assert skill.name == 'mysql'
        skill = SkillFactory(name=' java ', category=CATEGORY.programming_language)
        assert skill.name == 'java'
