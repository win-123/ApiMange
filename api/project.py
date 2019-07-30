#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/3  下午6:20

from schema import project
from sanic import Blueprint
from core.response import resp_json
from core.status import FAIL
import models
from utils.runner import DebugCode

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

    async def post(self, request):
        name = request.json.get("name", None)
        project_name = await self.model.filter(name=name).first()
        if project_name:
            return resp_json(FAIL, msg="项目已存在")
        result = {
            "name": name,
            "desc": request.json.get("desc"),
            "responsible": request.json.get("responsible"),
        }
        await models.Project.create(**result)
        return resp_json(msg="项目添加成功!")

    async def patch(self, request):
        name = request.json.get("name", None)
        pk = request.json.get("id")
        instance = await self.model.get_or_404(pk)

        if not instance:
            return resp_json(FAIL, msg="项目不存在！")
        if name != instance.name:
            if await models.Project.filter(name=name).first():
                return resp_json(FAIL, msg="项目已存在！")

        instance.name = name
        instance.desc = request.json.get("desc")
        schema = self.get_schema(request)
        result = schema.dump(instance)

        await instance.save()

        return resp_json(msg="请求成功", body=result.data)

    async def delete(self, request):
        pk = request.json.get("id")
        instance = await self.model.get_or_404(pk)
        if not instance:
            return resp_json(FAIL, msg="项目不存在！")
        await instance.delete()

        return resp_json(msg="操作成功！")


class ProjectDetailView(GenericAPIView):
    """
    获取项目详情
    """
    model = models.Project
    schema_class = project.ProjectDetailSchema

    async def get(self, request):
        pk = self.request.args.get("project_id")
        if not pk:
            return resp_json(FAIL, msg="项目不存在！")
        queryset = await self.model.filter(id=pk).first()
        api_count = await models.API.filter(project_id=pk).count()
        case_count = await models.Case.filter(project_id=pk).count()
        config_count = await models.Config.filter(project_id=pk).count()
        variables_count = await models.Variables.filter(project_id=pk).count()
        host_count = await models.HostIP.filter(project_id=pk).count()
        report_count = await models.Report.filter(project_id=pk).count()

        data = {
            "id": pk,
            "name": queryset.name,
            "desc": queryset.desc,
            "api_count": api_count,
            "case_count": case_count,
            "config_count": config_count,
            "variables_count": variables_count,
            "host_count": host_count,
            "report_count": report_count,
        }

        return resp_json(body=data)


class DebugTalkView(GenericAPIView):
    """
    DebugTalk
    """
    model = models.DebugTalk
    schema_class = project.DebugTalkSchema

    async def get(self, request):
        pk = self.request.args.get("project_id")
        if not pk:
            return resp_json(FAIL, msg="项目不存在！")
        code = await self.model.filter(project_id=pk)

        return resp_json(body=code)

    async def post(self, request):

        code = request.json[0].get("code")
        debug = DebugCode(code)
        debug.run()

        return resp_json(msg="项目运行成功!")

    async def patch(self, request):
        project_id = request.json.get("project_id")
        code = request.json.get("code")
        pro = await models.Project.filter(pk=project_id).first()

        result = {
            "code": code,
            "project": pro,
        }
        await models.DebugTalk.create(**result)

        return resp_json()


class TreeView(GenericAPIView):
    """
    树形结构操作
    """
    model = models.Relation
    schema_class = project.RelationSchema

    async def get(self, request):
        pk = self.request.args.get("project")
        queryset = await self.model.filter(project_id=pk, type=self.request.args.get("type"))

        schema = self.get_schema(request)
        result = schema.dump(queryset, many=True)

        return resp_json(body=result.data)


class ApiView(GenericAPIView):
    """
    api
    """
    model = models.API
    schema_class = project.ApiSchema

    async def get(self, request):
        pk = self.request.args.get("project")
        queryset = await self.model.filter(project_id=pk)

        schema = self.get_schema(request)
        result = schema.dump(queryset, many=True)

        return resp_json(body=result.data)


class ConfigView(GenericAPIView):
    """
    配置
    """
    model = models.Config
    schema_class = project.ConfigSchema

    async def get(self, request):
        pk = self.request.args.get("project")
        queryset = await self.model.filter(project_id=pk)

        schema = self.get_schema(request)
        result = schema.dump(queryset, many=True)

        return resp_json(body=result.data)

    async def post(self, request):
        project_id = request.json.get("project")
        pro = await models.Project.filter(pk=project_id).first()

        if not project_id:
            return resp_json(FAIL, msg="项目不存在")
        result = {
            "body": request.json,
            "name": request.json.get("name"),
            "base_url": request.json.get("base_url"),
            "project": pro,
        }
        await models.Config.create(**result)
        return resp_json(msg="项目添加成功!")

    async def patch(self, request):
        pk = request.json.get("variableData")['id']
        instance = await self.model.filter(pk=pk).first()
        if not instance:
            return resp_json(FAIL, msg="变量不存在！")
        instance.key = request.json.get("variableData")["key"]
        instance.value = request.json.get("variableData")["value"]

        schema = self.get_schema(request)
        result = schema.dump(instance)

        await instance.save()

        return resp_json(result.data)

    async def delete(self, request):

        if request.json.get("id"):
            pk = request.json.get("id")
        else:
            pk = request.json[0].get("id")

        instance = await self.model.get_or_404(pk)
        if not instance:
            return resp_json(FAIL, msg=" 变量不存在！")
        await instance.delete()

        return resp_json(msg="操作成功！")


class CaseView(GenericAPIView):
    """
    用例
    """
    model = models.Case
    schema_class = project.CaseSchema

    async def get(self, request):
        pk = self.request.args.get("project")
        queryset = await self.model.filter(project_id=pk)

        schema = self.get_schema(request)
        result = schema.dump(queryset, many=True)

        return resp_json(body=result.data)


class CaseStepView(GenericAPIView):
    """
    用例步骤
    """
    model = models.CaseStep
    schema_class = project.CaseStepSchema

    async def get(self, request):
        pk = self.request.args.get("project")
        queryset = await self.model.filter(project_id=pk)

        schema = self.get_schema(request)
        result = schema.dump(queryset, many=True)

        return resp_json(body=result.data)


class HostIPView(GenericAPIView):
    """
    主机
    """
    model = models.HostIP
    schema_class = project.HostIPSchema

    async def get(self, request):
        pk = self.request.args.get("project")
        queryset = await self.model.filter(project_id=pk)

        schema = self.get_schema(request)
        result = schema.dump(queryset, many=True)

        return resp_json(body=result.data)

    async def post(self, request):

        project_id = request.json.get("project")
        pro = await models.Project.filter(pk=project_id).first()

        if not project_id:
            return resp_json(FAIL, msg="项目不存在")
        result = {
            "value": request.json.get("value"),
            "name": request.json.get("name"),
            "project": pro,
        }
        await models.HostIP.create(**result)
        return resp_json(msg="项目添加成功!")

    async def patch(self, request):

        pk = request.json.get("hostData")['id']
        instance = await self.model.filter(pk=pk).first()
        if not instance:
            return resp_json(FAIL, msg="域名不存在！")
        instance.name = request.json.get("hostData")["name"]
        instance.value = request.json.get("hostData")["value"]

        schema = self.get_schema(request)
        result = schema.dump(instance)

        await instance.save()

        return resp_json(result.data)

    async def delete(self, request):
        pk = request.json.get("id")
        instance = await self.model.get_or_404(pk)
        if not instance:
            return resp_json(FAIL, msg="环境变量不存在！")
        await instance.delete()

        return resp_json(msg="操作成功！")


class VariablesView(GenericAPIView):
    """
    环境变量
    """
    model = models.Variables
    schema_class = project.VariablesSchema

    async def get(self, request):
        pk = self.request.args.get("project")
        queryset = await self.model.filter(project_id=pk)

        schema = self.get_schema(request)
        result = schema.dump(queryset, many=True)

        return resp_json(body=result.data)

    async def post(self, request):
        project_id = request.json.get("project")
        pro = await models.Project.filter(pk=project_id).first()

        if not project_id:
            return resp_json(FAIL, msg="项目不存在")
        result = {
            "value": request.json.get("value"),
            "key": request.json.get("key"),
            "project": pro,
        }
        await models.Variables.create(**result)
        return resp_json(msg="项目添加成功!")

    async def patch(self, request):
        pk = request.json.get("variableData")['id']
        instance = await self.model.filter(pk=pk).first()
        if not instance:
            return resp_json(FAIL, msg="变量不存在！")
        instance.key = request.json.get("variableData")["key"]
        instance.value = request.json.get("variableData")["value"]

        schema = self.get_schema(request)
        result = schema.dump(instance)

        await instance.save()

        return resp_json(result.data)

    async def delete(self, request):

        pk = request.json.get("id")
        instance = await self.model.get_or_404(pk)
        if not instance:
            return resp_json(FAIL, msg=" 变量不存在！")
        await instance.delete()

        return resp_json(msg="操作成功！")


class ReportView(GenericAPIView):
    """
    报告
    """
    model = models.Report
    schema_class = project.ReportSchema

    async def get(self, request):
        pk = self.request.args.get("project")
        queryset = await self.model.filter(project_id=pk)

        schema = self.get_schema(request)
        result = schema.dump(queryset, many=True)

        return resp_json(body=result.data)

    async def post(self, request):
        project_id = request.json.get("project")
        pro = await models.Project.filter(pk=project_id).first()

        if not project_id:
            return resp_json(FAIL, msg="项目不存在")
        result = {
            "value": request.json.get("value"),
            "name": request.json.get("name"),
            "project": pro,
        }
        await models.Report.create(**result)
        return resp_json(msg="报告添加成功!")

    async def patch(self, request):

        pk = request.json.get("hostData")['id']
        instance = await self.model.filter(pk=pk).first()
        if not instance:
            return resp_json(FAIL, msg="域名不存在！")
        instance.name = request.json.get("hostData")["name"]
        instance.value = request.json.get("hostData")["value"]

        schema = self.get_schema(request)
        result = schema.dump(instance)

        await instance.save()

        return resp_json(result.data)

    async def delete(self, request):
        pk = request.json.get("id")
        instance = await self.model.get_or_404(pk)
        if not instance:
            return resp_json(FAIL, msg="环境变量不存在！")
        await instance.delete()

        return resp_json(msg="操作成功！")


class ScheduleView(GenericAPIView):
    """
    定时任务
    """
    model = models.Schedule
    schema_class = project.ScheduleSchema

    async def get(self, request):
        pk = self.request.args.get("project")
        queryset = await self.model.filter(project_id=pk)

        schema = self.get_schema(request)
        result = schema.dump(queryset, many=True)

        return resp_json(body=result.data)

    async def post(self, request):
        project_id = request.json.get("project")
        pro = await models.Project.filter(pk=project_id).first()

        if not project_id:
            return resp_json(FAIL, msg="项目不存在")
        result = {
            "name": request.json.get("name"),
            "identity": request.json.get("data"),
            "status": request.json.get("switch"),
            "send_type": request.json.get("strategy"),
            "config": request.json.get("corntab"),
            "receiver": request.json.get("receiver"),
            "copy": request.json.get("copy"),
            "project": pro,
        }
        await models.Schedule.create(**result)
        return resp_json(msg="报告添加成功!")
    #
    # async def patch(self, request):
    #
    #     pk = request.json.get("hostData")['id']
    #     instance = await self.model.filter(pk=pk).first()
    #     if not instance:
    #         return resp_json(FAIL, msg="域名不存在！")
    #     instance.name = request.json.get("hostData")["name"]
    #     instance.value = request.json.get("hostData")["value"]
    #
    #     schema = self.get_schema(request)
    #     result = schema.dump(instance)
    #
    #     await instance.save()
    #
    #     return resp_json(result.data)
    #
    # async def delete(self, request):
    #     pk = request.json.get("id")
    #     instance = await self.model.get_or_404(pk)
    #     if not instance:
    #         return resp_json(FAIL, msg="环境变量不存在！")
    #     await instance.delete()
    #
    #     return resp_json(msg="操作成功！")


bp.add_route(ProjectView.as_view(), '/project/')
bp.add_route(ProjectDetailView.as_view(), '/pro_detail/')
bp.add_route(DebugTalkView.as_view(), '/debugtalk/')
bp.add_route(TreeView.as_view(), '/tree/')
bp.add_route(ApiView.as_view(), '/api/')
bp.add_route(ConfigView.as_view(), '/config/')
bp.add_route(CaseView.as_view(), '/case/')
bp.add_route(CaseStepView.as_view(), '/case_step/')
bp.add_route(HostIPView.as_view(), '/host_ip/')
bp.add_route(VariablesView.as_view(), '/variables/')
bp.add_route(ReportView.as_view(), '/reports/')
bp.add_route(ScheduleView.as_view(), '/schedule/')
