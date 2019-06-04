from rest_framework.serializers import ModelSerializer

from ssm.events.models import Event, FAQ


class StaffEventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class EventSerializer(StaffEventSerializer):

    class Meta(StaffEventSerializer.Meta):
        read_only_fields = '__all__'


class StaffFAQSerializer(ModelSerializer):

    class Meta:
        model = FAQ
        fields = '__all__'


class FAQSerializer(StaffFAQSerializer):

    class Meta(StaffFAQSerializer.Meta):
        read_only_fields = '__all__'
