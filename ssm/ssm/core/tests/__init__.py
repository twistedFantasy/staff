from faker import Faker
from django.urls import reverse
from rest_framework.test import APITestCase


EXCLUDE = ['password', 'skills']


class BaseTestCase(APITestCase):  # FIXME: remove?
    list_url = None
    detail_url = None

    @classmethod
    def setUpTestData(cls):
        cls.fake = Faker()

    def get_list_url(self):
        return reverse(self.list_url)

    def get_detail_url(self, entity_id):
        return reverse(self.detail_url, args=[entity_id])

    def assert_fields(self, entity, data, user):
        for field in data.keys():
            if field not in EXCLUDE:
                assert getattr(entity, field) == (user if field == 'user' else data[field])
