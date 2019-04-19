from ssm.core.filters import ObjectFieldFilterBackend


class ProjectFilterBackend(ObjectFieldFilterBackend):
    field = 'id'
    filter_field = 'membersmodel__user__id'
    object = 'request.user'
