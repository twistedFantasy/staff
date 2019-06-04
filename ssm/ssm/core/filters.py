from rest_framework.filters import BaseFilterBackend


class ObjectFieldFilterBackend(BaseFilterBackend):
    field = 'id'
    filter_field = 'id'
    object = 'request.user'

    def filter_queryset(self, request, queryset, view):
        is_staff = request.user.is_staff
        field = request.query_params.get(self.field) if is_staff else getattr(eval(self.object), self.field)
        if field:
            return queryset.filter(**{f'{self.filter_field}': field})
        return queryset
