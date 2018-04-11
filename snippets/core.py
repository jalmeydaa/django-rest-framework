from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param


class CustomPaginator(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_number(),
            'previous': self.get_previous_number(),
            'courses': data
        })

    def get_next_number(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_number(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return replace_query_param('', self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return replace_query_param('', self.page_query_param, page_number)
