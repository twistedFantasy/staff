from django.test import TestCase
from ssm.skills.models import Skill, CATEGORY


class SkillTestCase(TestCase):

    def test_name_field_should_be_lowercase(self):
        skill = Skill.objects.create(name='PYTHON', category=CATEGORY.programming_language)
        assert skill.name == 'python'
        skill = Skill.objects.create(name='PostgreSQL', category=CATEGORY.database)
        assert skill.name == 'postgresql'
        skill = Skill.objects.create(name='golang', category=CATEGORY.programming_language)
        assert skill.name == 'golang'
        skill = Skill.objects.create(name=' mongodb', category=CATEGORY.database)
        assert skill.name == 'mongodb'
        skill = Skill.objects.create(name='mysql ', category=CATEGORY.database)
        assert skill.name == 'mysql'
        skill = Skill.objects.create(name=' java ', category=CATEGORY.programming_language)
        assert skill.name == 'java'
