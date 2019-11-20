from datetime import date

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, \
    HTTP_403_FORBIDDEN

from ssm.events.models import Event
from ssm.events.tests.factories import EventFactory
from ssm.events.serializers import StaffEventSerializer, EventSerializer
from ssm.users.tests.factories import StaffUserFactory, UserFactory
from ssm.core.helpers import Day
from ssm.core.tests import BaseTestCase


class EventViewSetTestCase(BaseTestCase):
    list_url = 'event-list'
    detail_url = 'event-detail'

    @classmethod
    def setUpTestData(cls):
        cls.staff_user = StaffUserFactory()
        cls.simple_user = UserFactory()
        super().setUpTestData()

    def test_permission_classes__only_is_authenticated_user_allows_access(self):
        [EventFactory() for _ in range(2)]
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_401_UNAUTHORIZED
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_permission_classes__staff_allow_to_use_any_rest_method(self):
        self.client.force_authenticate(self.staff_user)

        # POST
        assert Event.objects.count() == 0
        data = {
            'title': self.fake.text(),
            'description': self.fake.text(),
            'start_date': Day(ago=40).date,
            'end_date': Day(ago=35).date,
            'active': self.fake.boolean()
        }
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_201_CREATED
        assert response.data['title'] == data['title']
        assert Event.objects.count() == 1
        event = Event.objects.first()
        self.assert_fields(event, data, self.staff_user)

        # GET(id)
        response = self.client.get(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_200_OK
        serializer = StaffEventSerializer(event)
        assert response.data == serializer.data

        # PATCH
        data = {'title': self.fake.text()}
        response = self.client.patch(self.get_detail_url(response.data['id']), data=data)
        event.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['title'] == data['title']
        assert event.title == data['title']

        # PUT
        data = {**response.data, **{'title': self.fake.text()}}
        response = self.client.put(self.get_detail_url(response.data['id']), data=data)
        event.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['title'] == data['title']
        assert event.title == data['title']

        # DELETE
        response = self.client.delete(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_204_NO_CONTENT
        assert Event.objects.count() == 0

        # GET(all)
        [EventFactory() for _ in range(3)]
        events = Event.objects.all()
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 3
        serializer = StaffEventSerializer(events, many=True)
        assert response.data['results'] == serializer.data
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in events)

    def test_permission_classes__non_staff_allow_to_use_subset_of_rest_api_methods(self):
        self.client.force_authenticate(self.simple_user)
        event = EventFactory(active=True)
        event.refresh_from_db()

        # POST
        assert Event.objects.count() == 1
        data = {
            'title': self.fake.text(),
            'description': self.fake.text(),
            'start_date': Day(ago=40).date,
            'end_date': Day(ago=35).date,
            'active': self.fake.boolean()
        }
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_403_FORBIDDEN
        assert Event.objects.count() == 1

        # GET(id)
        response = self.client.get(self.get_detail_url(event.id))
        assert response.status_code == HTTP_200_OK
        serializer = EventSerializer(event)
        assert response.data == serializer.data

        # PATCH
        data = {'title': self.fake.text()}
        response = self.client.patch(self.get_detail_url(event.id), data=data)
        event.refresh_from_db()
        assert response.status_code == HTTP_403_FORBIDDEN
        assert event.title != data['title']

        # PUT
        data = {**response.data, **{'title': self.fake.text()}}
        response = self.client.put(self.get_detail_url(event.id), data=data)
        event.refresh_from_db()
        assert response.status_code == HTTP_403_FORBIDDEN
        assert event.title != data['title']

        # DELETE
        response = self.client.delete(self.get_detail_url(event.id))
        assert response.status_code == HTTP_403_FORBIDDEN
        assert Event.objects.count() == 1

        # GET(all)
        [EventFactory(active=active) for active in [True, False, True]]
        events = Event.objects.filter(active=True)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 3
        serializer = EventSerializer(events, many=True)
        assert response.data['results'] == serializer.data
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in events)

    def test_get_serializer_class__staff_event_serializer(self):
        event = EventFactory()
        event.refresh_from_db()
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.get_detail_url(event.id))
        serializer = StaffEventSerializer(event)
        assert response.status_code == HTTP_200_OK
        assert response.data == serializer.data

    def test_get_serializer_class__event_serializer(self):
        event = EventFactory(active=True)
        event.refresh_from_db()
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(self.get_detail_url(event.id))
        serializer = EventSerializer(event)
        assert response.status_code == HTTP_200_OK
        assert response.data == serializer.data

    def test_get_serializer_class__staff_user_allow_to_modify_all_fields(self):
        event = EventFactory()
        self.client.force_authenticate(self.staff_user)
        data = {
            'title': self.fake.text(),
            'description': self.fake.text(),
            'start_date': Day(ago=40).date,
            'end_date': Day(ago=35).date,
            'active': self.fake.boolean()
        }
        response = self.client.patch(self.get_detail_url(event.id), data=data)
        event.refresh_from_db()
        for field in data.keys():
            assert response.data[field] == (format(data[field]) if isinstance(data[field], date) else data[field])
            assert getattr(event, field) == data[field]

    def test_get_queryset__staff_user_see_all_events(self):
        [EventFactory(active=active) for active in [True, False, True]]
        self.client.force_authenticate(self.staff_user)
        events = Event.objects.all()
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 3
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in events)

    def test_get_queryset__non_staff_see_only_active_events(self):
        self.client.force_authenticate(self.simple_user)
        [EventFactory(active=active) for active in [True, False, True]]
        events = Event.objects.filter(active=True)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in events)
