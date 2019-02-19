from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ssm.skills.models import Skill
from ssm.skills.serializers import SkillWithUsersSerializer
from ssm.core.permissions import IsStaff


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillWithUsersSerializer
    permission_classes = [IsAuthenticated, IsStaff]
