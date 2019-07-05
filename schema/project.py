#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/3  下午6:35

import re

from marshmallow import fields
from marshmallow import validates
from marshmallow import ValidationError


from .base import BasicSchema


class ProjectSchema(BasicSchema):
    """
    项目
    """
    id = fields.Integer()
    name = fields.String()
    desc = fields.String()
    responsible = fields.String()


class DebugTalkSchema(BasicSchema):
    """
    DebugTalk
    """
    code = fields.String()


class RelationSchema(BasicSchema):
    """
    树形结构
    """
    tree = fields.String()
    type = fields.String()


class ApiSchema(BasicSchema):
    """
    树形结构
    """
    name = fields.String()
    body = fields.String()
    url = fields.String()
    method = fields.String()
    relation = fields.Integer()


class ConfigSchema(BasicSchema):
    """
    树形结构
    """
    name = fields.String()
    body = fields.String()
    base_url = fields.String()


class CaseSchema(BasicSchema):
    """
    用例
    """
    name = fields.String()
    tag = fields.String()
    count = fields.Integer()
    relation = fields.Integer()


class CaseStepSchema(BasicSchema):
    """
    用例步骤
    """
    name = fields.String()
    body = fields.String()
    url = fields.String()
    method = fields.String()
    step = fields.Integer()


class HostIPSchema(BasicSchema):
    """
    主机
    """
    name = fields.String()
    value = fields.String()


class VariablesSchema(BasicSchema):
    """
    变量
    """
    key = fields.String()
    value = fields.String()


class ReportSchema(BasicSchema):
    """
    报告
    """
    name = fields.String()
    type = fields.String()
    summary = fields.String()
