import pytest
from django.core import mail
from django.test import TestCase
from django.conf import settings

from ssm.users.models import BIRTHDAY, ASSESSMENT
from ssm.users.tests.factories import UserFactory
from ssm.core.helpers import today, Day


class UserTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory(email='UserTestCase@gmail.com')

    def test_str(self):
        assert str(self.user) == f'{self.user.get_full_name()} (user {self.user.id})'

    def test_is_birthday__true(self):
        self.user.date_of_birth = today()
        assert self.user.is_birthday()

    def test_is_birthday__false__already_notified(self):
        self.user.date_of_birth = today()
        self.user.birthday_notification = today()
        assert not self.user.is_birthday()

    def test_is_birthday__false_5_days_ago(self):
        self.user.date_of_birth = Day(ago=5).date
        assert not self.user.is_birthday()

    def test_is_birthday__false_5_days_ahead(self):
        self.user.date_of_birth = Day(ago=-5).date
        assert not self.user.is_birthday()

    def test_notify__birthday(self):
        self.user.notify(BIRTHDAY)
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == settings.BIRTHDAY_SUBJECT
        assert mail.outbox[0].body == settings.BIRTHDAY_MESSAGE

    def test_notify__assessment(self):
        self.user.notify(ASSESSMENT)
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == settings.ASSESSMENT_SUBJECT
        assert mail.outbox[0].body == settings.ASSESSMENT_MESSAGE

    def test_notify__unknown_notification(self):
        with pytest.raises(Exception):
            self.user.notify('unknown')
