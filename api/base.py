#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/3  下午6:21

"""
    api基类
"""

from sanic.views import HTTPMethodView

from core import exceptions
from core.pagination import LimitOffsetPagination


class GenericAPIView(HTTPMethodView):
    """
    拓展原有视图类
    """

    # 模型
    model = None
    # 序列化器
    schema_class = None
    # 分页器
    pagination_class = LimitOffsetPagination
    # 过滤器
    filter_backends = ()
    # 权限
    permission_classes = ()
    # 节流
    throttle_classes = ()

    # 初始化默认变量
    request = None

    def get_queryset(self):
        assert self.model is not None, (
                f"'{self.__class__.__name__}' should either include a `model` attribute, "
                "or override the `get_queryset()` method."
        )
        return self.model.all()

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def dispatch_request(self, request, *args, **kwargs):
        setattr(self, 'request', request)

        # 检测权限
        self.check_permissions(request)

        return super(GenericAPIView, self).dispatch_request(self.request, *args, **kwargs)

    def get_schema_class(self):
        """
        Return the class to use for the schema.
        Defaults to using `self.schema_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        return self.schema_class

    def get_schema_context(self, request):
        """
        Extra context provided to the schema class.
        """
        return {
            'request': request,
            'view': self
        }

    def get_schema(self, request, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        schema_class = self.get_schema_class()
        kwargs['context'] = self.get_schema_context(request)
        return schema_class(*args, **kwargs)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        return [permission() for permission in self.permission_classes]

    def get_throttles(self):
        """
        Instantiates and returns the list of throttles that this view uses.
        """
        return [throttle() for throttle in self.throttle_classes]

    def check_permissions(self, request):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(message=getattr(permission, 'message', None))

    def permission_denied(self, message):
        raise exceptions.PermissionDenied(message=message)

    def check_throttles(self, request):
        """
        Check if request should be throttled.
        Raises an appropriate exception if the request is throttled.
        """
        for throttle in self.get_throttles():
            if not throttle.allow_request(request, self):
                self.throttled(request, throttle.wait())

    def throttled(self, request, wait):
        """
        If request is throttled, determine what kind of exception to raise.
        """
        raise exceptions.Throttled(wait)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                setattr(self, "_paginator", None)
            else:
                setattr(self, "_paginator", self.pagination_class())

        return getattr(self, "_paginator", None)

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request)


