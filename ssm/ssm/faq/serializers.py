from rest_framework.serializers import ModelSerializer

from ssm.faq.models import FAQ


class StaffFAQSerializer(ModelSerializer):

    class Meta:
        model = FAQ
        fields = '__all__'


class FAQSerializer(StaffFAQSerializer):

    class Meta(StaffFAQSerializer.Meta):
        read_only_fields = '__all__'
