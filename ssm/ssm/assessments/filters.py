from django_filters.rest_framework import FilterSet

from ssm.assessments.models import Checkpoint, Task
from ssm.core.filters import ObjectFieldFilterBackend


class CheckpointFilterBackend(ObjectFieldFilterBackend):
    filter_field = 'assessment__user__id'


class TaskFilterBackend(ObjectFieldFilterBackend):
    filter_field = 'checkpoint__assessment__user__id'


class CheckpointFilter(FilterSet):

    class Meta:
        model = Checkpoint
        fields = ['assessment', 'date']


class TaskFilter(FilterSet):

    class Meta:
        model = Task
        fields = ['checkpoint', 'completed']
