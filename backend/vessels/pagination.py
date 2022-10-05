from functools import cached_property
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class ResultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        '''Remove links and count from paginated response in order to enhance performance'''
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'results': data
        })