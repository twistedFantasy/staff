from rest_framework.serializers import ModelSerializer

from ssm.events.models import Event, FAQ


class StaffEventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class EventSerializer(StaffEventSerializer):

    class Meta(StaffEventSerializer.Meta):
        read_only_fields = ['title', 'description', 'start_date', 'end_date', 'notify', 'to', 'active']


class StaffFAQSerializer(ModelSerializer):

    class Meta:
        model = FAQ
        fields = '__all__'


class FAQSerializer(StaffFAQSerializer):

    class Meta(StaffFAQSerializer.Meta):
        read_only_fields = ['question', 'answer', 'order', 'active']
