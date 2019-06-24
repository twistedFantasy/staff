from faker import Faker
from django.test import TestCase

from ssm.events.tests.factories import EventFactory, FAQFactory
from ssm.events.serializers import StaffEventSerializer, EventSerializer, StaffFAQSerializer, FAQSerializer, \
    EVENT_FIELDS, FAQ_FIELDS
from ssm.core.helpers import Day


class StaffEventSerializerTestCase(TestCase):

    def test__model_fields(self):
        event = EventFactory()
        serializer = StaffEventSerializer(event)
        for field in EVENT_FIELDS:
            assert serializer.data[field] == getattr(event, field)

    def test__empty_read_only_fields(self):
        event = EventFactory(start_date=Day().date, end_date=Day().date, notify=True, active=True)
        data = {
            'title': 'Test',
            'description': 'Test',
            'start_date': Day(ago=5).date,
            'end_date': Day(ago=5).date,
            'notify': False,
            'to': 'twisteeed.fantasy@gmail.com',
            'active': False,
        }
        serializer = StaffEventSerializer(event, data=data)
        assert serializer.is_valid()
        event = serializer.save()
        for field in data.keys():
            assert getattr(event, field) == data[field]


class EventSerializerTestCase(TestCase):

    def test__read_only_fields(self):
        event = EventFactory(start_date=Day().date, end_date=Day().date, notify=True, active=True)
        data = {
            'title': 'Test',
            'description': 'Test',
            'start_date': Day(ago=5).date,
            'end_date': Day(ago=5).date,
            'notify': False,
            'to': 'twisteeed.fantasy@gmail.com',
            'active': False,
        }
        serializer = EventSerializer(event, data=data)
        assert serializer.is_valid()
        event = serializer.save()
        for field in data.keys():
            assert getattr(event, field) != data[field]


class StaffFAQSerializerTestCase(TestCase):

    def test__model_fields(self):
        faq = FAQFactory()
        faq.refresh_from_db()
        serializer = StaffFAQSerializer(faq)
        for field in FAQ_FIELDS:
            assert serializer.data[field] == getattr(faq, field)

    def test__empty_read_only_fields(self):
        faq = FAQFactory(order=2, active=True)
        data = {'question': 'Test', 'answer': 'Test', 'order': 4, 'active': False}
        serializer = StaffFAQSerializer(faq, data=data)
        assert serializer.is_valid()
        faq = serializer.save()
        for field in data.keys():
            assert getattr(faq, field) == data[field]


class FAQSerializerTestCase(TestCase):

    def test__read_only_fields(self):
        faq = FAQFactory(order=2, active=True)
        data = {'question': 'Test', 'answer': 'Test', 'order': 4, 'active': False}
        serializer = FAQSerializer(faq, data=data)
        assert serializer.is_valid()
        faq = serializer.save()
        for field in data.keys():
            assert getattr(faq, field) != data[field]
