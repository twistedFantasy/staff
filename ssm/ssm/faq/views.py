from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ssm.faq.models import FAQ
from ssm.faq.serializers import StaffFAQSerializer, FAQSerializer
from ssm.core.permissions import IsAllowedMethodOrStaff


class FAQViewSet(ModelViewSet):
    queryset = FAQ.objects.all()
    permission_classes = [IsAuthenticated, IsAllowedMethodOrStaff]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ['question', 'answer']
    ordering_fields = ['order']

    def get_serializer_class(self):
        return StaffFAQSerializer if self.request.user.is_staff else FAQSerializer

    def get_queryset(self):
        return FAQ.objects.all() if self.request.user.is_staff else FAQ.objects.filter(active=True)
