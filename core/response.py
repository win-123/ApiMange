#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/3  下午7:10

from sanic.response import json

from .status import (
    SUCCESS
)


def resp_json(code=SUCCESS, msg="请求成功", body=None):

    body = {
        "code": code,
        "msg": msg,
        "data": body or []
    }

    return json(body)
