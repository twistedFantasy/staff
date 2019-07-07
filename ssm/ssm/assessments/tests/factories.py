from factory import DjangoModelFactory, Faker, SubFactory

from ssm.assessments.models import Assessment, Checkpoint, Task, STATUS
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


class CheckpointFactory(DjangoModelFactory):

    class Meta:
        model = Checkpoint

    assessment = SubFactory(AssessmentFactory)
    title = Faker('word')
    date = Faker('date')


class TaskFactory(DjangoModelFactory):

    class Meta:
        model = Task

    checkpoint = SubFactory(CheckpointFactory)
    title = Faker('word')
    description = Faker('text')
    completed = Faker('boolean')
