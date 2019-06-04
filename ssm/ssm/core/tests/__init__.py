from django.urls import reverse
from django.conf import settings
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APITestCase

from ssm.users.models import User


class BaseTestCase(APITestCase):
    endpoint = None

    def setUp(self):
        data = {'email': settings.TEST_STAFFUSER_EMAIL, 'password': settings.TEST_STAFFUSER_PASSWORD}
        self.staff_user = User.objects.create_superuser(**data)
        data = {'email': settings.TEST_SIMPLEUSER_EMAIL, 'password': settings.TEST_SIMPLEUSER_PASSWORD}
        self.simple_user = User.objects.create_user(**data)

    def test_permission_classes__only_is_authenticated_user_allows_access(self):
        if self.endpoint:
            response = self.client.get(reverse(self.endpoint))
            assert response.status_code == HTTP_401_UNAUTHORIZED
            self.client.force_authenticate(self.simple_user)
            response = self.client.get(reverse(self.endpoint))
            assert response.status_code == HTTP_200_OK
