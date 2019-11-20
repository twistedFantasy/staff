from django.test import TestCase

from ssm.events.tests.factories import EventFactory


class EventTestCase(TestCase):

    def test__str(self):
        event = EventFactory()
        assert str(event) == f'{event.title} (event {event.id})'
