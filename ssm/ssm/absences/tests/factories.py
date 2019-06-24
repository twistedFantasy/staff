from factory import DjangoModelFactory, Faker, SubFactory

from ssm.absences.models import Absence, STATUS, REASON
from ssm.users.tests.factories import UserFactory


class AbsenceFactory(DjangoModelFactory):

    class Meta:
        model = Absence

    user = SubFactory(UserFactory)
    decision_by = SubFactory(UserFactory)
    reason = Faker('random_element', elements=[REASON.vacation, REASON.illness, REASON.other])
    status = Faker('random_element', elements=[STATUS.new, STATUS.verifying])
    start_date = Faker('date')
    end_date = Faker('date')
    notes = Faker('text')
