from ssm.core.filters import ObjectFieldFilterBackend


class ProjectFilterBackend(ObjectFieldFilterBackend):
    filter_field = 'membersmodel__user__id'
