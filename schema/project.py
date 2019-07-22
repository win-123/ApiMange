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
    create_time = fields.DateTime()
    update_time = fields.DateTime()


class ProjectDetailSchema(BasicSchema):
    """
    项目
    """
    id = fields.Integer()
    name = fields.String()
    desc = fields.String()
    responsible = fields.String()
    create_time = fields.DateTime()
    update_time = fields.DateTime()


class DebugTalkSchema(BasicSchema):
    """
    DebugTalk
    """
    id = fields.Integer()
    code = fields.String()
    create_time = fields.DateTime()
    update_time = fields.DateTime()


class RelationSchema(BasicSchema):
    """
    树形结构
    """
    id = fields.Integer()
    tree = fields.String()
    type = fields.String()
    maxId = fields.Method(method_name="get_max_id")
    create_time = fields.DateTime()
    update_time = fields.DateTime()

    def get_max_id(self, instance):
        if not instance.id:
            return 0
        for i in eval(instance.tree):

            if not i["children"]:
                return max(i["id"])

            for j in i["children"]:
                return j["id"]


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
    create_time = fields.DateTime()
    update_time = fields.DateTime()


class ConfigSchema(BasicSchema):
    """
    树形结构
    """
    id = fields.Integer()
    name = fields.String()
    body = fields.String()
    base_url = fields.String()
    create_time = fields.DateTime()
    update_time = fields.DateTime()


class CaseSchema(BasicSchema):
    """
    用例
    """
    id = fields.Integer()
    name = fields.String()
    tag = fields.String()
    length = fields.Integer()
    relation = fields.Integer()
    create_time = fields.DateTime()
    update_time = fields.DateTime()


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
    create_time = fields.DateTime()
    update_time = fields.DateTime()


class HostIPSchema(BasicSchema):
    """
    主机
    """
    id = fields.Integer()
    name = fields.String()
    value = fields.String()
    create_time = fields.DateTime()
    update_time = fields.DateTime()


class VariablesSchema(BasicSchema):
    """
    变量
    """
    id = fields.Integer()
    key = fields.String()
    value = fields.String()
    create_time = fields.DateTime()
    update_time = fields.DateTime()


class ReportSchema(BasicSchema):
    """
    报告
    """
    id = fields.Integer()
    name = fields.String()
    type = fields.String()
    summary = fields.String()
    create_time = fields.DateTime()
    update_time = fields.DateTime()


class ScheduleSchema(BasicSchema):
    """
    报告
    """
    id = fields.Integer()
    name = fields.String()
    identity = fields.String()
    send_type = fields.Integer()
    config = fields.String()
    receiver = fields.String()
    copy = fields.String()
    status = fields.Integer()
    create_time = fields.DateTime()
    update_time = fields.DateTime()
