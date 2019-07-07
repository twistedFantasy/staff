from ssm.core.filters import ObjectFieldFilterBackend


class CheckpointFilterBackend(ObjectFieldFilterBackend):
    filter_field = 'assessment__user__id'


class TaskFilterBackend(ObjectFieldFilterBackend):
    filter_field = 'checkpoint__assessment__user__id'
