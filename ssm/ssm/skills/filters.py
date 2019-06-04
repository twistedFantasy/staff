from ssm.core.filters import ObjectFieldFilterBackend


class SkillFilterBackend(ObjectFieldFilterBackend):
    filter_field = 'userskillmodel__user__id'
