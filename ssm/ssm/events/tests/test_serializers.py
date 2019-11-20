from faker import Faker
from django.test import TestCase

from ssm.events.tests.factories import EventFactory
from ssm.events.serializers import StaffEventSerializer, EventSerializer
from ssm.core.helpers import Day


class StaffEventSerializerTestCase(TestCase):

    def test__model_fields(self):
        event = EventFactory()
        serializer = StaffEventSerializer(event)
        for field in ['id', 'title', 'description', 'start_date', 'end_date', 'notify', 'to', 'active']:
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
