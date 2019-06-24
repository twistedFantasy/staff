from rest_framework.serializers import ModelSerializer

from ssm.events.models import Event, FAQ


EVENT_FIELDS = ['id', 'title', 'description', 'start_date', 'end_date', 'notify', 'to', 'active']
FAQ_FIELDS = ['id', 'question', 'answer', 'order', 'active']


class StaffEventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = EVENT_FIELDS


class EventSerializer(StaffEventSerializer):

    class Meta(StaffEventSerializer.Meta):
        read_only_fields = EVENT_FIELDS


class StaffFAQSerializer(ModelSerializer):

    class Meta:
        model = FAQ
        fields = FAQ_FIELDS


class FAQSerializer(StaffFAQSerializer):

    class Meta(StaffFAQSerializer.Meta):
        read_only_fields = FAQ_FIELDS
