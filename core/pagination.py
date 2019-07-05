#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/3  下午6:25

from collections import OrderedDict


def _get_count(queryset):
    """
    Determine an object count, supporting either querysets or regular lists.
    """
    try:
        return queryset.count()
    except (AttributeError, TypeError):
        return len(queryset)


def _positive_int(integer_string, strict=False, cutoff=None):
    """
    Cast a string to a strictly positive integer.
    """
    ret = int(integer_string)
    if ret < 0 or (ret == 0 and strict):
        raise ValueError()
    if cutoff:
        ret = min(ret, cutoff)
    return ret


class BasePagination(object):
    ...


class LimitOffsetPagination(BasePagination):
    """
    A limit/offset based style. For example:

    http://api.example.org/accounts/?limit=100
    http://api.example.org/accounts/?offset=400&limit=100
    """
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100

    def __init__(self):
        self.count, self.limit, self.offset, self.request = None, None, None, None

    def paginate_queryset(self, queryset, request):
        self.count = _get_count(queryset)
        self.limit = self.get_limit(request)

        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        self.request = request

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset:self.offset + self.limit])

    def get_limit(self, request):
        if self.limit_query_param:
            try:
                return _positive_int(
                    request.raw_args[self.limit_query_param],
                    strict=True,
                    cutoff=self.max_limit
                )
            except (KeyError, ValueError):
                pass

        return self.default_limit

    def get_offset(self, request):
        try:
            return _positive_int(
                request.raw_args[self.offset_query_param],
            )
        except (KeyError, ValueError):
            return 0

    def get_paginated_data(self, data):
        return OrderedDict([
            ('count', self.count),
            ('results', data)
        ])
