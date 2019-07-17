#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/3  下午6:35

import re
import models
from marshmallow import fields
from marshmallow import validates
from marshmallow import ValidationError
from utils import prepare


from .base import BasicSchema


class ProjectSchema(BasicSchema):
    """
    项目
    """
    id = fields.Integer()
    name = fields.String()
    desc = fields.String()
    responsible = fields.String()


class ProjectDetailSchema(BasicSchema):
    """
    项目
    """
    id = fields.Integer()
    name = fields.String()
    desc = fields.String()
    responsible = fields.String()
    count = fields.Method(method_name="get_project_detail_count")

    def get_project_detail_count(self, instance):

        result = prepare.get_project_detail(instance.pk)

        return result


class DebugTalkSchema(BasicSchema):
    """
    DebugTalk
    """
    id = fields.Integer()
    code = fields.String()


class RelationSchema(BasicSchema):
    """
    树形结构
    """
    id = fields.Integer()
    tree = fields.String()
    type = fields.String()


class ApiSchema(BasicSchema):
    """
    树形结构
    """
    id = fields.Integer()
    name = fields.String()
    body = fields.String()
    url = fields.String()
    method = fields.String()
    relation = fields.Integer()


class ConfigSchema(BasicSchema):
    """
    树形结构
    """
    id = fields.Integer()
    name = fields.String()
    body = fields.String()
    base_url = fields.String()


class CaseSchema(BasicSchema):
    """
    用例
    """
    id = fields.Integer()
    name = fields.String()
    tag = fields.String()
    count = fields.Integer()
    relation = fields.Integer()


class CaseStepSchema(BasicSchema):
    """
    用例步骤
    """
    id = fields.Integer()
    name = fields.String()
    body = fields.String()
    url = fields.String()
    method = fields.String()
    step = fields.Integer()


class HostIPSchema(BasicSchema):
    """
    主机
    """
    id = fields.Integer()
    name = fields.String()
    value = fields.String()


class VariablesSchema(BasicSchema):
    """
    变量
    """
    id = fields.Integer()
    key = fields.String()
    value = fields.String()


class ReportSchema(BasicSchema):
    """
    报告
    """
    id = fields.Integer()
    name = fields.String()
    type = fields.String()
    summary = fields.String()
