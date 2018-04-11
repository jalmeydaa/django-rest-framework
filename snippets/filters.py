
from rest_framework.filters import BaseFilterBackend


class SnippetBackendFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        params = request.query_params

        if params.get('ids'):
            queryset.filter(id__in=params.get('ids').split(','))

        return queryset
