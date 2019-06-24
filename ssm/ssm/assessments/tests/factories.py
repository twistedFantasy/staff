from factory import DjangoModelFactory, Faker, SubFactory

from ssm.assessments.models import Assessment, STATUS
from ssm.users.tests.factories import UserFactory


class AssessmentFactory(DjangoModelFactory):

    class Meta:
        model = Assessment

    user = SubFactory(UserFactory)
    decision_by = SubFactory(UserFactory)
    status = Faker('random_element', elements=STATUS)
    start_date = Faker('date')
    end_date = Faker('date')
    plan = Faker('text')
    comments = Faker('text')
    notes = Faker('text')
