from factory import DjangoModelFactory, Faker

from ssm.events.models import Event, FAQ


class EventFactory(DjangoModelFactory):

    class Meta:
        model = Event

    title = Faker('word')
    description = Faker('text')
    start_date = Faker('date')
    end_date = Faker('date')
    notify = Faker('boolean')
    to = Faker('email')
    active = Faker('boolean')


class FAQFactory(DjangoModelFactory):

    class Meta:
        model = FAQ

    question = Faker('word')
    answer = Faker('text')
    order = Faker('random_number')
    active = Faker('boolean')
