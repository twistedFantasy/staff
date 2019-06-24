from datetime import date

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, \
    HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from ssm.assessments.models import Assessment, STATUS
from ssm.assessments.serializers import StaffAssessmentSerializer, AssessmentSerializer
from ssm.users.tests.factories import UserFactory, StaffUserFactory
from ssm.assessments.tests.factories import AssessmentFactory
from ssm.core.tests import BaseTestCase
from ssm.core.helpers import Day, format


class AssessmentViewSetTestCase(BaseTestCase):
    list_url = 'assessment-list'
    detail_url = 'assessment-detail'

    def setUp(self):
        self.staff_user = StaffUserFactory()
        self.simple_user = UserFactory()

    def test_permission_classes__only_is_authenticated_user_allows_access(self):
        [AssessmentFactory(user=user) for user in [self.staff_user, self.simple_user]]
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_401_UNAUTHORIZED
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_permission_classes__staff_allow_to_use_any_rest_method(self):
        self.client.force_authenticate(self.staff_user)

        # POST
        assert Assessment.objects.count() == 0
        data = {
            'user': {'id': self.staff_user.id, 'email': self.staff_user.email},
            'status': STATUS.in_progress,
            'start_date': Day(ago=40).date,
            'end_date': Day(ago=35).date,
        }
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_201_CREATED
        assert response.data['status'] == data['status']
        assert Assessment.objects.count() == 1
        assessment = Assessment.objects.first()
        self.assert_fields(assessment, data, self.staff_user)

        # GET(id)
        response = self.client.get(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_200_OK
        serializer = StaffAssessmentSerializer(assessment)
        assert response.data == serializer.data

        # PATCH
        data = {'status': STATUS.completed}
        response = self.client.patch(self.get_detail_url(response.data['id']), data=data)
        assessment.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['status'] == data['status']
        assert assessment.status == data['status']

        # PUT
        data = {**response.data, **{'status': STATUS.completed}}
        response = self.client.put(self.get_detail_url(response.data['id']), data=data)
        assessment.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['status'] == data['status']
        assert assessment.status == data['status']

        # DELETE
        response = self.client.delete(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_204_NO_CONTENT
        assert Assessment.objects.count() == 0

        # GET(all)
        [AssessmentFactory(user=user) for user in [self.staff_user] + [self.simple_user] * 2]
        assessments = Assessment.objects.all()
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 3
        serializer = StaffAssessmentSerializer(assessments, many=True)
        assert response.data['results'] == serializer.data
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in assessments)

    def test_permission_classes__non_staff_allow_to_use_subset_of_rest_api_methods(self):
        self.client.force_authenticate(self.simple_user)
        assessment = AssessmentFactory(user=self.simple_user)
        assessment.refresh_from_db()

        # POST
        assert Assessment.objects.count() == 1
        data = {
            'user': {'id': self.simple_user.id, 'email': self.simple_user.email},
            'status': STATUS.new,
            'start_date': Day(ago=40).date,
            'end_date': Day(ago=35).date,
        }
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_403_FORBIDDEN
        assert Assessment.objects.count() == 1

        # GET(id)
        response = self.client.get(self.get_detail_url(assessment.id))
        assert response.status_code == HTTP_200_OK
        serializer = AssessmentSerializer(assessment)
        assert response.data == serializer.data

        # PATCH
        data = {'status': STATUS.in_progress}
        response = self.client.patch(self.get_detail_url(assessment.id), data=data)
        assessment.refresh_from_db()
        assert response.status_code == HTTP_403_FORBIDDEN
        assert assessment.status != data['status']

        # PUT
        data = {**response.data, **{'status': STATUS.failed}}
        response = self.client.put(self.get_detail_url(assessment.id), data=data)
        assessment.refresh_from_db()
        assert response.status_code == HTTP_403_FORBIDDEN
        assert assessment.status != data['status']

        # DELETE
        response = self.client.delete(self.get_detail_url(assessment.id))
        assert response.status_code == HTTP_403_FORBIDDEN
        assert Assessment.objects.count() == 1

        # GET(all)
        [AssessmentFactory(user=user) for user in [self.staff_user, self.simple_user]]
        assessments = Assessment.objects.filter(user=self.simple_user)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        serializer = AssessmentSerializer(assessments, many=True)
        assert response.data['results'] == serializer.data
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in assessments)

    def test_permission_classes__staff_allows_to_access_and_modify_any_other_users_data(self):
        self.client.force_authenticate(self.staff_user)

        # POST
        assert Assessment.objects.count() == 0
        data = {
            'user': {'id': self.simple_user.id, 'email': self.simple_user.email},
            'status': STATUS.new,
            'start_date': Day(ago=40).date,
            'end_date': Day(ago=35).date,
        }
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_201_CREATED
        assert response.data['status'] == data['status']
        assessment = Assessment.objects.first()
        self.assert_fields(assessment, data, self.simple_user)

        # GET(id)
        response = self.client.get(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_200_OK
        serializer = StaffAssessmentSerializer(assessment)
        assert response.data == serializer.data

        # PATCH
        data = {'status': STATUS.in_progress}
        response = self.client.patch(self.get_detail_url(response.data['id']), data=data)
        assessment.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['status'] == data['status']
        assert assessment.status == data['status']

        # PUT
        data = {**response.data, **{'status': STATUS.completed}}
        response = self.client.put(self.get_detail_url(response.data['id']), data=data)
        assessment.refresh_from_db()
        assert response.status_code == HTTP_200_OK
        assert response.data['status'] == data['status']
        assert assessment.status == data['status']

        # DELETE
        response = self.client.delete(self.get_detail_url(response.data['id']))
        assert response.status_code == HTTP_204_NO_CONTENT
        assert Assessment.objects.count() == 0

        # GET(all)
        [AssessmentFactory(user=user) for user in [self.simple_user, self.staff_user, self.simple_user]]
        assessments = Assessment.objects.all()
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 3
        serializer = StaffAssessmentSerializer(assessments, many=True)
        assert response.data['results'] == serializer.data
        assert set(entity['id'] for entity in response.data['results']) == set(entity.id for entity in assessments)

    def test_permission_classes__non_staff_allows_to_access_only_his_data(self):
        self.client.force_authenticate(self.simple_user)
        assessment = AssessmentFactory(user=self.staff_user)

        # POST
        assert Assessment.objects.count() == 1
        data = {
            'user': {'id': self.staff_user.id, 'email': self.staff_user.email},
            'status': STATUS.new,
            'start_date': Day(ago=40).date,
            'end_date': Day(ago=35).date,
        }
        response = self.client.post(self.get_list_url(), data=data)
        assert response.status_code == HTTP_403_FORBIDDEN
        assert Assessment.objects.count() == 1

        # GET(id)
        response = self.client.get(self.get_detail_url(assessment.id))
        assert response.status_code == HTTP_404_NOT_FOUND

        # PATCH
        data = {'status': STATUS.in_progress}
        response = self.client.patch(self.get_detail_url(assessment.id), data=data)
        assert response.status_code == HTTP_403_FORBIDDEN

        # DELETE
        response = self.client.delete(self.get_detail_url(assessment.id))
        assert response.status_code == HTTP_403_FORBIDDEN

        # GET(all)
        [AssessmentFactory(user=user) for user in [self.simple_user] * 2 + [self.staff_user]]
        assessments = Assessment.objects.filter(user=self.simple_user)
        response = self.client.get(self.get_list_url())
        assert response.status_code == HTTP_200_OK
        assert len(response.data['results']) == 2
        assert Assessment.objects.count() == 4
        serializer = StaffAssessmentSerializer(assessments, many=True)
        assert response.data['results'] == serializer.data

    def test_get_serializer_class__staff_assessment_serializer(self):
        assessment = AssessmentFactory()
        assessment.refresh_from_db()
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.get_detail_url(assessment.id))
        serializer = StaffAssessmentSerializer(assessment)
        assert response.status_code == HTTP_200_OK
        assert response.data == serializer.data

    def test_get_serializer_class__assessment_serializer(self):
        assessment = AssessmentFactory(user=self.simple_user)
        assessment.refresh_from_db()
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(self.get_detail_url(assessment.id))
        serializer = AssessmentSerializer(assessment)
        assert response.status_code == HTTP_200_OK
        assert response.data == serializer.data

    def test_get_serializer_class__staff_user_allow_to_modify_all_fields(self):
        assessment = AssessmentFactory(status=STATUS.new, start_date=Day().date, end_date=Day().date)
        self.client.force_authenticate(self.staff_user)
        user, decision_by = UserFactory(), UserFactory()
        data = {
            'user': {'id': user.id},
            'decision_by': {'id': decision_by.id},
            'status': STATUS.completed,
            'start_date': Day(ago=15).date,
            'end_date': Day(ago=10).date,
            'plan': self.fake.text(),
            'comments': self.fake.text(),
            'notes': self.fake.text(),
        }
        response = self.client.patch(self.get_detail_url(assessment.id), data=data)
        assessment.refresh_from_db()
        assert assessment.user.id == data['user']['id']
        assert assessment.decision_by.id == data['decision_by']['id']
        assert response.data['user']['id'] == data['user']['id']
        assert response.data['decision_by']['id'] == data['decision_by']['id']
        data.pop('user'), data.pop('decision_by')
        for field in data.keys():
            assert response.data[field] == (format(data[field]) if isinstance(data[field], date) else data[field])
            assert getattr(assessment, field) == data[field]

    def test_get_serializer_class_non_staff_user_allow_to_modify_non_read_only_fields(self):
        assessment = AssessmentFactory(user=self.simple_user, start_date=Day().date, end_date=Day().date)
        self.client.force_authenticate(self.simple_user)
        user, decision_by = UserFactory(), UserFactory()
        data = {
            'user': {'id': user.id},
            'decision_by': {'id': decision_by.id},
            'status': STATUS.completed,
            'start_date': Day(ago=15).date,
            'end_date': Day(ago=10).date,
            'plan': self.fake.text(),
            'comments': self.fake.text(),
            'notes': self.fake.text(),
        }
        response = self.client.patch(self.get_detail_url(assessment.id), data=data)
        assert response.status_code == HTTP_403_FORBIDDEN
        assessment.refresh_from_db()
        assert assessment.user.id != data['user']['id']
        assert assessment.decision_by.id != data['decision_by']['id']
        data.pop('user'), data.pop('decision_by')
        for field in data.keys():
            assert getattr(assessment, field) != data[field]
