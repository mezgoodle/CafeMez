from rest_framework.pagination import LimitOffsetPagination


class Paginator(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
    offset_query_param = 'offset'
    limit_query_param = 'limit'
