#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/3  下午6:20

import os
import json
from schema import project
from sanic import Blueprint
from core.response import resp_json
from core.status import FAIL
import models

from .base import GenericAPIView

bp = Blueprint('project', url_prefix='/api')


class ProjectView(GenericAPIView):
    """
    项目类api
    """
    model = models.Project
    schema_class = project.ProjectSchema

    async def get(self, request):
        queryset = await self.model.all()

        schema = self.get_schema(request)
        result = schema.dump(queryset, many=True)

        return resp_json(body=result.data)


class DebugTalkView(GenericAPIView):
    """
    DebugTalk
    """
    model = models.DebugTalk
    schema_class = project.DebugTalkSchema

    async def get(self, request):
        return resp_json(msg="请求成功")


class TreeView(GenericAPIView):
    """
    树形结构操作
    """
    model = models.Relation
    schema_class = project.RelationSchema


class ApiView(GenericAPIView):
    """
    api
    """
    model = models.API
    schema_class = project.ApiSchema


class ConfigView(GenericAPIView):
    """
    配置
    """
    model = models.Config
    schema_class = project.ConfigSchema


class CaseView(GenericAPIView):
    """
    用例
    """
    model = models.Case
    schema_class = project.CaseSchema


class CaseStepView(GenericAPIView):
    """
    用例步骤
    """
    model = models.CaseStep
    schema_class = project.CaseStepSchema


class HostIPView(GenericAPIView):
    """
    主机
    """
    model = models.HostIP
    schema_class = project.HostIPSchema


class VariablesView(GenericAPIView):
    """
    环境变量
    """
    model = models.Variables
    schema_class = project.VariablesSchema


class ReportView(GenericAPIView):
    """
    报告
    """
    model = models.Report
    schema_class = project.ReportSchema


bp.add_route(ProjectView.as_view(), '/project/')
bp.add_route(DebugTalkView.as_view(), '/debugtalk/')
bp.add_route(TreeView.as_view(), '/tree/')
bp.add_route(ApiView.as_view(), '/api/')
bp.add_route(ConfigView.as_view(), '/config/')
bp.add_route(CaseView.as_view(), '/case/')
bp.add_route(CaseStepView.as_view(), '/case_step/')
bp.add_route(HostIPView.as_view(), '/host/')
bp.add_route(VariablesView.as_view(), '/variables/')
bp.add_route(ReportView.as_view(), '/report/')
