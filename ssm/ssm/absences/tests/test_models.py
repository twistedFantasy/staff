import pytest
from django.test import TestCase

from ssm.absences.models import STATUS, REASON
from ssm.absences.tests.factories import AbsenceFactory


class AbsenceTestCase(TestCase):

    def absence_str(self, absence):
        return f'{absence.user.id if absence.user else "-"} (absences {absence.id})'

    def test__str_with_user(self):
        absence = AbsenceFactory()
        assert str(absence) == self.absence_str(absence)

    def test__str_holiday_without_user(self):
        absense = AbsenceFactory(reason=REASON.holiday, user=None)
        assert str(absense) == self.absence_str(absense)

    def test__save_holiday_reason_with_user(self):
        with pytest.raises(ValueError):
            AbsenceFactory(reason=REASON.holiday)

    def test__save_holiday_reason_without_user(self):
        try:
            absence = AbsenceFactory(reason=REASON.holiday, user=None)
            assert absence.id
        except Exception as e:
            pytest.fail(str(e))

    def test__save_move_to_approved(self):
        try:
            absence = AbsenceFactory()
            absence.modify(status=STATUS.approved)
        except Exception as e:
            pytest.fail(str(e))

    def test__save_move_to_approved_without_start_date(self):
        with pytest.raises(ValueError):
            absence = AbsenceFactory(start_date=None)
            absence.modify(status=STATUS.approved)

    def test__save_move_to_approved_without_end_date(self):
        with pytest.raises(ValueError):
            absence = AbsenceFactory(end_date=None)
            absence.modify(status=STATUS.approved)

    def test__save_move_to_approved_without_start_and_end_dates(self):
        with pytest.raises(ValueError):
            absence = AbsenceFactory(start_date=None, end_date=None)
            absence.modify(status=STATUS.approved)
