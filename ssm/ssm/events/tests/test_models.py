from django.test import TestCase

from ssm.events.tests.factories import EventFactory, FAQFactory


class EventTestCase(TestCase):

    def test__str(self):
        event = EventFactory()
        assert str(event) == f'{event.title} (event {event.id})'


class FAQTestCase(TestCase):

    def test__str(self):
        faq = FAQFactory()
        assert str(faq) == f'{faq.question} (faq {faq.id})'
