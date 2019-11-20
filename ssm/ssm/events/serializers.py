from rest_framework.serializers import ModelSerializer

from ssm.events.models import Event


EVENT_FIELDS = ['id', 'title', 'description', 'start_date', 'end_date', 'notify', 'to', 'active']


class StaffEventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = EVENT_FIELDS


class EventSerializer(StaffEventSerializer):

    class Meta(StaffEventSerializer.Meta):
        read_only_fields = EVENT_FIELDS
