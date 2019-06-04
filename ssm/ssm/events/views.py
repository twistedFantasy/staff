from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from ssm.events.models import Event
from ssm.events.serializers import StaffEventSerializer, EventSerializer
from ssm.core.permissions import IsAllowedMethodOrStaff


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, IsAllowedMethodOrStaff]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'description', 'start_date', 'end_date']

    def get_serializer_class(self):
        return StaffEventSerializer if self.request.is_staff else EventSerializer

    def get_queryset(self):
        return Event.objects.all() if self.request.user.is_staff else Event.objects.filter(active=True)
