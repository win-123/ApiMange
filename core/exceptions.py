#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/3  下午6:24

from sanic.exceptions import SanicException

from .status import (
    FAIL, LOGIN
)


class APIException(SanicException):
    """
    Api异常
    """

    code = FAIL

    def __init__(self, message, extra_data=None):
        super().__init__(message)

        self.message = message
        self.extra_data = extra_data or {}


class AuthenticationFailed(APIException):
    """
    认证失败类
    """
    ...


class Throttled(APIException):
    """
    节流控制
    """
    ...


class PermissionDenied(APIException):
    """
    权限认证
    """
    code = LOGIN
