from factory import DjangoModelFactory, Faker, SubFactory, RelatedFactory

from ssm.projects.models import Project, MembersModel, STATUS, ROLES
from ssm.users.tests.factories import UserFactory


class ProjectFactory(DjangoModelFactory):

    class Meta:
        model = Project

    name = Faker('word')
    description = Faker('text')
    start_date = Faker('date')
    end_date = Faker('date')
    status = Faker('random_element', elements=[STATUS.waiting, STATUS.in_progress])


class MembersModelFactory(DjangoModelFactory):

    class Meta:
        model = MembersModel

    user = SubFactory(UserFactory)
    project = SubFactory(ProjectFactory)
    role = Faker('random_element', elements=list(ROLES))
    joined_date = Faker('date')
    left_date = Faker('date')


class UserWith3ProjectsFactory(UserFactory):
    membership1 = RelatedFactory(MembersModelFactory, 'user', project__name=Faker('word'))
    membership2 = RelatedFactory(MembersModelFactory, 'user', project__name=Faker('word'))
    membership3 = RelatedFactory(MembersModelFactory, 'user', project__name=Faker('word'))


class ProjectWith3UsersFactory(ProjectFactory):
    membership1 = RelatedFactory(MembersModelFactory, 'project', user__email=Faker('email'))
    membership2 = RelatedFactory(MembersModelFactory, 'project', user__email=Faker('email'))
    membership3 = RelatedFactory(MembersModelFactory, 'project', user__email=Faker('email'))
