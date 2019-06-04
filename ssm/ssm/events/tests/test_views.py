from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

from ssm.events.models import Event, FAQ
from ssm.core.tests import BaseTestCase


class EventViewSetTestCase(BaseTestCase):
    endpoint = 'event-list'

    @classmethod
    def setUpTestData(cls):
        Event.objects.create(title='Test Event1', description='Test Description1')
        data = {'title': 'Test Event2', 'description': 'Test Description2', 'active': True}
        Event.objects.create(**data)

    def setUp(self):
        self.data = {'title': 'Test Event', 'description': 'Test Description', 'active': True}
        self.event = Event.objects.create(**self.data)
        super().setUp()

    def test_permission_classes__staff_allow_to_use_any_rest_method(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(reverse('event-list'))
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 3
        response = self.client.get(reverse('event-detail', args=[self.event.id]))
        assert response.status_code == HTTP_200_OK
        assert response.data['title'] == self.event.title
        response = self.client.patch(reverse('event-detail', args=[self.event.id]), data={'title': 'New Test Event'})
        assert response.status_code == HTTP_200_OK
        assert response.data['title'] == 'New Test Event'
        data = {'title': 'New Test Event', 'description': 'New Test Description', 'active': True}
        response = self.client.post(reverse('event-list'), data=data)
        assert response.status_code == HTTP_201_CREATED
        assert response.data['title'] == data['title']
        response = self.client.delete(reverse('event-detail', args=[response.data['id']]))
        assert response.status_code == HTTP_204_NO_CONTENT

    def test_permission_classes__non_staff_allow_to_use_subset_of_rest_api_methods(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('event-list'))
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        response = self.client.get(reverse('event-detail', args=[self.event.id]))
        assert response.status_code == HTTP_200_OK
        assert response.data['title'] == self.event.title
        response = self.client.patch(reverse('event-detail', args=[self.event.id]), data={'title': 'New Test Event'})
        assert response.status_code == HTTP_403_FORBIDDEN
        data = {'title': 'New Test Event', 'description': 'New Test Description', 'active': True}
        response = self.client.post(reverse('event-list'), data=data)
        assert response.status_code == HTTP_403_FORBIDDEN
        response = self.client.delete(reverse('event-detail', args=[self.event.id]))
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_get_serializer_class__staff_user(self):
        data = {'title': 'New Test Event', 'description': 'New Test Description', 'active': False}
        assert self.event.title != data['title']
        assert self.event.description != data['description']
        assert self.event.active
        self.client.force_authenticate(self.staff_user)
        response = self.client.patch(reverse('event-detail', args=[self.event.id]), data)
        assert response.data['title'] == data['title']
        assert response.data['description'] == data['description']
        assert not response.data['active']

    def test_get_serializer_class_non_staff_user(self):
        data = {'title': 'New Test Event', 'description': 'New Test Description', 'active': False}
        assert self.event.title != data['title']
        assert self.event.description != data['description']
        assert self.event.active
        self.client.force_authenticate(self.simple_user)
        response = self.client.patch(reverse('event-detail', args=[self.event.id]), data)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_get_queryset__staff_user_return_all_events(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(reverse('event-list'))
        assert len(response.data['results']) == 3

    def test_get_queryset__non_staff_user_return_only_active_events(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('event-list'))
        assert len(response.data['results']) == 2


class FAQViewSetTestCase(BaseTestCase):
    endpoint = 'faq-list'

    @classmethod
    def setUpTestData(cls):
        cls.data1 = {'question': 'Test Question1', 'answer': 'Test Answer1', 'order': 4, 'active': True}
        FAQ.objects.create(**cls.data1)
        FAQ.objects.create(question='Test Question2', answer='Test Answer2', order=12)

    def setUp(self):
        self.data = {'question': 'Test Question', 'answer': 'Test Answer', 'order': 2, 'active': True}
        self.faq = FAQ.objects.create(**self.data)
        super().setUp()

    def test_permission_classes__staff_allow_to_use_any_rest_method(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(reverse('faq-list'))
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 3
        assert response.data['results'][0]['question'] == self.data['question']
        assert response.data['results'][0]['order'] == self.data['order']
        assert response.data['results'][1]['question'] == self.data1['question']
        assert response.data['results'][1]['order'] == self.data1['order']
        response = self.client.get(reverse('faq-detail', args=[self.faq.id]))
        assert response.status_code == HTTP_200_OK
        assert response.data['question'] == self.faq.question
        response = self.client.patch(reverse('faq-detail', args=[self.faq.id]), data={'question': 'New Test Question'})
        assert response.status_code == HTTP_200_OK
        assert response.data['question'] == 'New Test Question'
        data = {'question': 'New Test Question', 'answer': 'New Test Answer', 'order': 1, 'active': True}
        response = self.client.post(reverse('faq-list'), data=data)
        assert response.status_code == HTTP_201_CREATED
        assert response.data['question'] == data['question']
        response = self.client.delete(reverse('faq-detail', args=[response.data['id']]))
        assert response.status_code == HTTP_204_NO_CONTENT

    def test_permission_classes__non_staff_allow_to_use_subset_of_rest_api_methods(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('faq-list'))
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        response = self.client.get(reverse('faq-detail', args=[self.faq.id]))
        assert response.status_code == HTTP_200_OK
        assert response.data['question'] == self.faq.question
        response = self.client.patch(reverse('faq-detail', args=[self.faq.id]), data={'question': 'New Test Question'})
        assert response.status_code == HTTP_403_FORBIDDEN
        data = {'question': 'New Test Question', 'answer': 'New Test Answer', 'order': 1, 'active': True}
        response = self.client.post(reverse('faq-list'), data=data)
        assert response.status_code == HTTP_403_FORBIDDEN
        response = self.client.delete(reverse('faq-detail', args=[self.faq.id]))
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_get_serializer_class__staff_user(self):
        data = {'question': 'New Test Question', 'answer': 'New Test Answer', 'active': False}
        assert self.faq.question != data['question']
        assert self.faq.answer != data['answer']
        assert self.faq.active
        self.client.force_authenticate(self.staff_user)
        response = self.client.patch(reverse('faq-detail', args=[self.faq.id]), data)
        assert response.data['question'] == data['question']
        assert response.data['answer'] == data['answer']
        assert not response.data['active']

    def test_get_serializer_class_non_staff_user(self):
        data = {'question': 'New Test Question', 'answer': 'New Test Answer', 'active': False}
        assert self.faq.question != data['question']
        assert self.faq.answer != data['answer']
        assert self.faq.active
        self.client.force_authenticate(self.simple_user)
        response = self.client.patch(reverse('faq-detail', args=[self.faq.id]), data)
        response.status_code == HTTP_403_FORBIDDEN

    def test_get_queryset__staff_user_return_all_faq(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(reverse('faq-list'))
        assert len(response.data['results']) == 3

    def test_get_queryset__non_staff_user_return_only_active_faq(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('faq-list'))
        assert len(response.data['results']) == 2
