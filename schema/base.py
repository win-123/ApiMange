#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/3  下午6:36

from marshmallow import Schema


class BasicSchema(Schema):

    class Meta:
        # 使用 `OrderedDict`, 让字段变的有序
        ordered = True
        # 更多属性请参阅源码...
