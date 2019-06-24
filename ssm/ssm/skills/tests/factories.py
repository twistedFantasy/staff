from factory import DjangoModelFactory, Faker, SubFactory, RelatedFactory

from ssm.skills.models import Skill, UserSkillModel
from ssm.users.tests.factories import UserFactory


class SkillFactory(DjangoModelFactory):

    class Meta:
        model = Skill


class UserSkillModelFactory(DjangoModelFactory):

    class Meta:
        model = UserSkillModel

    user = SubFactory(UserFactory)
    skill = SubFactory(SkillFactory)
    notes = Faker('text')

#
# class SkillWith3Users(DjangoModelFactory):
#     userskillmodel1 = RelatedFactory(UserSkillModelFactory, 'user1', skill__name='python')
#     userskillmodel2 = RelatedFactory(UserSkillModelFactory, 'user2', skill__name='python')
#     userskillmodel3 = RelatedFactory(UserSkillModelFactory, 'user3', skill__name='python')
