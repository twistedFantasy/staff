from django.test import TestCase
from faker import Faker

from ssm.absences.models import STATUS, REASON
from ssm.absences.serializers import StaffAbsenceSerializer, AbsenceSerializer, FIELDS
from ssm.absences.tests.factories import AbsenceFactory
from ssm.users.tests.factories import UserFactory
from ssm.core.helpers import Day


class StaffAbsenceSerializerTestCase(TestCase):

    def test__model_fields(self):
        absence = AbsenceFactory()
        serializer = StaffAbsenceSerializer(absence)
        for field in FIELDS:
            if field not in ['user', 'decision_by']:
                assert serializer.data[field] == getattr(absence, field)

    def test__empty_read_only_fields(self):
        absence = AbsenceFactory(status=STATUS.new, reason=REASON.illness, start_date=Day().date, end_date=Day().date)
        user = UserFactory()
        data = {
            'user': {'id': user.id},
            'status': STATUS.verifying,
            'reason': REASON.other,
            'start_date': Day(ago=5).date,
            'end_date': Day(ago=4).date,
            'notes': 'Test notes',
        }
        serializer = StaffAbsenceSerializer(absence, data=data)
        assert serializer.is_valid()
        absence = serializer.save()
        assert absence.user.id == data['user']['id']
        data.pop('user')
        for field in data.keys():
            assert getattr(absence, field) == data[field]


class AbsenceSerializerTestCase(TestCase):

    def test__read_only_fields(self):
        absence = AbsenceFactory(status=STATUS.new, reason=REASON.illness, start_date=Day().date, end_date=Day().date)
        user, decision_by = UserFactory(), UserFactory()
        data = {
            'user': {'id': user.id},
            'decision_by': {'id': decision_by.id},
            'status': STATUS.verifying,
            'reason': REASON.other,
            'start_date': Day(ago=5).date,
            'end_date': Day(ago=4).date,
            'notes': 'Test notes',
        }
        serializer = AbsenceSerializer(absence, data=data)
        assert serializer.is_valid()
        absence = serializer.save()
        assert absence.user.id == data['user']['id']
        assert absence.decision_by.id != data['decision_by']['id']
        assert absence.notes != data['notes']
        data.pop('user'), data.pop('decision_by'), data.pop('notes')
        for field in data.keys():
            assert getattr(absence, field) == data[field]
