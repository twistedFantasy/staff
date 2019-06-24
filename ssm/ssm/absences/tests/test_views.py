from datetime import date

from django.db.models import Q
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, \
    HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from ssm.absences.models import Absence, REASON, STATUS
from ssm.absences.serializers import StaffAbsenceSerializer, AbsenceSerializer
from ssm.absences.tests.factories import AbsenceFactory
from ssm.users.tests.factories import StaffUserFactory, UserFactory
from ssm.core.tests import BaseTestCase
from ssm.core.helpers import Day, format


class AbsenceViewSetTestCase(BaseTestCase):
    list_url = 'absence-list'
    detail_url = 'absence-detail'

    def setUp(self):
        self.staff_user = StaffUserFactory()
        self.simple_user = UserFactory()

    def test_permission_classes__only_is_authenticated_user_allows_access(self):
        [AbsenceFactory(user=user) for user in [self.staff_user, self.simple_user]]
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_401_UNAUTHORIZED
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_permission_classes__staff_allow_to_use_any_rest_method(self):
        self.client.force_authenticate(self.staff_user)

        # POST
        assert Absence.objects.count() == 0
        data = {
            'user': {'id': self.staff_user.id, 'email': self.staff_user.email},
            'reason': REASON.illness,
            'start_date': Day(ago=40).date,
            'end_date': Day(ago=35).date,
        }
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_201_CREATED
        assert Absence.objects.count() == 1
        absence = Absence.objects.first()
        self.assert_fields(absence, data, self.staff_user)

        # GET(id)
        response = self.client.get(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_200_OK
        assert response.data['reason'] == data['reason']
        serializer = StaffAbsenceSerializer(absence)
        assert response.data == serializer.data

        # PATCH
        data = {'reason': REASON.other}
        response = self.client.patch(self.get_detail_url(response.data['id']), data=data)
        absence.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['reason'] == data['reason']
        assert absence.reason == data['reason']

        # PUT
        data = {**response.data, **{'reason': REASON.illness}}
        response = self.client.put(self.get_detail_url(response.data['id']), data=data)
        absence.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['reason'] == data['reason']
        assert absence.reason == data['reason']

        # DELETE
        response = self.client.delete(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_204_NO_CONTENT
        assert Absence.objects.count() == 0

        # GET(all)
        [AbsenceFactory(user=user) for user in [self.staff_user] + [self.simple_user] * 2]
        absences = Absence.objects.all()
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 3
        serializer = StaffAbsenceSerializer(absences, many=True)
        assert response.data['results'] == serializer.data
        assert set(absence['id'] for absence in response.data['results']) == set(absence.id for absence in absences)

    def test_permission_classes__non_staff_allow_to_use_subset_of_rest_api_methods(self):
        self.client.force_authenticate(self.simple_user)

        # POST
        assert Absence.objects.count() == 0
        data = {
            'user': {'id': self.simple_user.id, 'email': self.simple_user.email},
            'status': STATUS.new,
            'reason': REASON.illness,
            'start_date': Day(ago=40).date,
            'end_date': Day(ago=35).date,
        }
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_201_CREATED
        assert response.data['status'] == data['status']
        assert Absence.objects.count() == 1
        absence = Absence.objects.first()
        self.assert_fields(absence, data, self.simple_user)

        # GET(id)
        response = self.client.get(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_200_OK
        serializer = AbsenceSerializer(absence)
        assert response.data == serializer.data

        # PATCH
        data = {'reason': REASON.other}
        response = self.client.patch(self.get_detail_url(response.data['id']), data=data)
        absence.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['reason'] == data['reason']
        assert absence.reason == data['reason']

        # PUT
        data = {**response.data, **{'reason': REASON.illness}}
        response = self.client.put(self.get_detail_url(response.data['id']), data=data)
        absence.refresh_from_db()
        assert response.status_code == HTTP_403_FORBIDDEN
        assert absence.reason != data['reason']

        # DELETE
        response = self.client.delete(self.get_detail_url(absence.id))
        assert response.status_code == HTTP_403_FORBIDDEN
        assert Absence.objects.count() == 1

        # GET(all)
        [AbsenceFactory(user=user) for user in [self.staff_user, self.simple_user]]
        absences = Absence.objects.filter(user=self.simple_user)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        serializer = AbsenceSerializer(absences, many=True)
        assert response.data['results'] == serializer.data
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in absences)

    def test_permission_classes__staff_allows_to_access_and_modify_any_other_users_data(self):
        self.client.force_authenticate(self.staff_user)

        # POST
        assert Absence.objects.count() == 0
        data = {
            'user': {'id': self.simple_user.id, 'email': self.simple_user.email},
            'reason': REASON.illness,
            'start_date': Day(ago=40).date,
            'end_date': Day(ago=35).date,
        }
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_201_CREATED
        assert response.data['reason'] == data['reason']
        absence = Absence.objects.first()
        self.assert_fields(absence, data, self.simple_user)

        # GET(id)
        response = self.client.get(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_200_OK
        serializer = StaffAbsenceSerializer(absence)
        assert response.data == serializer.data

        # PATCH
        data = {'reason': REASON.other}
        response = self.client.patch(self.get_detail_url(response.data['id']), data=data)
        absence.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['reason'] == data['reason']
        assert absence.reason == data['reason']

        # PUT
        data = {**response.data, **{'reason': REASON.illness}}
        response = self.client.put(self.get_detail_url(response.data['id']), data=data)
        absence.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['reason'] == data['reason']
        assert absence.reason == data['reason']

        # DELETE
        response = self.client.delete(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_204_NO_CONTENT
        assert Absence.objects.count() == 0

        # GET(all)
        [AbsenceFactory(user=user) for user in [self.simple_user, self.staff_user, self.simple_user]]
        absences = Absence.objects.all()
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 3
        serializer = StaffAbsenceSerializer(absences, many=True)
        assert response.data['results'] == serializer.data
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in absences)

    def test_permission_classes__non_staff_allows_to_access_and_modify_only_his_data(self):
        self.client.force_authenticate(self.simple_user)
        absence = AbsenceFactory(user=self.staff_user)

        # POST
        assert Absence.objects.count() == 1
        data = {
            'user': {'id': self.staff_user.id, 'email': self.staff_user.email},
            'reason': REASON.illness,
            'start_date': Day(ago=40).date,
            'end_date': Day(ago=35).date,
        }
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_403_FORBIDDEN
        assert Absence.objects.count() == 1

        # GET(id)
        response = self.client.get(self.get_detail_url(absence.id))
        assert response.status_code == HTTP_404_NOT_FOUND

        # PATCH
        data = {'reason': REASON.other}
        response = self.client.patch(self.get_detail_url(absence.id), data=data)
        assert response.status_code == HTTP_404_NOT_FOUND

        # DELETE
        response = self.client.delete(self.get_detail_url(absence.id))
        assert response.status_code == HTTP_403_FORBIDDEN

        # GET(all)
        [AbsenceFactory(user=user) for user in [self.simple_user] * 2 + [self.staff_user]]
        absences = Absence.objects.filter(user=self.simple_user)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        assert Absence.objects.count() == 4
        serializer = StaffAbsenceSerializer(absences, many=True)
        assert response.data['results'] == serializer.data

    def test_get_serializer_class__staff_absence_serializer(self):
        absence = AbsenceFactory()
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.get_detail_url(absence.id))
        serializer = StaffAbsenceSerializer(absence)
        assert response.status_code == HTTP_200_OK
        assert response.data == serializer.data

    def test_get_serializer_class__absence_serializer(self):
        absence = AbsenceFactory(user=self.simple_user)
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(self.get_detail_url(absence.id))
        serializer = AbsenceSerializer(absence)
        assert response.status_code == HTTP_200_OK
        assert response.data == serializer.data

    def test_get_serializer_class__staff_user_allow_to_modify_all_fields(self):
        absence = AbsenceFactory(status=STATUS.new, reason=REASON.illness, start_date=Day().date, end_date=Day().date)
        self.client.force_authenticate(self.staff_user)
        user, decision_by = UserFactory(), UserFactory()
        data = {
            'user': {'id': user.id},
            'decision_by': {'id': decision_by.id},
            'status': STATUS.verifying,
            'reason': REASON.other,
            'start_date': Day(ago=5).date,
            'end_date': Day(ago=4).date,
            'notes': self.fake.text(),
        }
        response = self.client.patch(self.get_detail_url(absence.id), data=data)
        absence.refresh_from_db()
        assert absence.user.id == data['user']['id']
        assert absence.decision_by.id == data['decision_by']['id']
        assert response.data['user']['id'] == data['user']['id']
        assert response.data['decision_by']['id'] == data['decision_by']['id']
        data.pop('user'), data.pop('decision_by')
        for field in data.keys():
            assert response.data[field] == (format(data[field]) if isinstance(data[field], date) else data[field])
            assert getattr(absence, field) == data[field]

    def test_get_serializer_class_non_staff_user_allow_to_modify_non_read_only_fields(self):
        data = {
            'user': self.simple_user,
            'status': STATUS.new,
            'reason': REASON.illness,
            'start_date': Day().date,
            'end_date': Day().date,
        }
        absence = AbsenceFactory(**data)
        self.client.force_authenticate(self.simple_user)
        user, decision_by = UserFactory(), UserFactory()
        data = {
            'user': {'id': user.id},
            'decision_by': {'id': decision_by.id},
            'status': STATUS.verifying,
            'reason': REASON.other,
            'start_date': Day(ago=5).date,
            'end_date': Day(ago=4).date,
            'notes': self.fake.text(),
        }
        response = self.client.patch(self.get_detail_url(absence.id), data=data)
        assert response.status_code == HTTP_403_FORBIDDEN
        absence.refresh_from_db()
        assert absence.user.id != data['user']['id']
        assert absence.decision_by.id != data['decision_by']['id']
        data.pop('user'), data.pop('decision_by')
        for field in data.keys():
            assert getattr(absence, field) != data[field]
        data = {
            'status': STATUS.verifying,
            'reason': REASON.other,
            'start_date': Day(ago=5).date,
            'end_date': Day(ago=4).date,
        }
        response = self.client.patch(self.get_detail_url(absence.id), data=data)
        assert response.status_code == HTTP_200_OK
        absence.refresh_from_db()
        for field in data.keys():
            assert getattr(absence, field) == data[field]

    def test_get_queryset__staff_user_see_all_absences(self):
        self.client.force_authenticate(self.staff_user)
        [AbsenceFactory(user=user) for user in [self.simple_user, self.staff_user, self.simple_user]]
        absences = Absence.objects.all()
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 3
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in absences)

    def test_get_queryset__non_staff_see_only_his_data_or_holiday(self):
        self.client.force_authenticate(self.simple_user)
        AbsenceFactory(user=None, reason=REASON.holiday)
        [AbsenceFactory(user=user) for user in [self.simple_user, self.staff_user, self.simple_user]]
        absences = Absence.objects.filter(Q(user=self.simple_user) | Q(reason=REASON.holiday))
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 3
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in absences)