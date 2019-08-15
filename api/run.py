#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/22  下午2:58

from sanic import Blueprint
from core.response import resp_json
from utils import loader
from httprunner.api import HttpRunner
import models
from utils.host import parse_host

from .base import GenericAPIView

bp = Blueprint('run', url_prefix='/api')


class RunApiView(GenericAPIView):
    """
    运行api by id
    """
    async def get(self, request):
        api = await models.API.filter(id=self.request.args.get("id")).first()
        config = await models.Config.filter(name=self.request.args.get("config")).first()

        pro = await models.Project.filter(pk=api.project_id).first()

        debug_talk = await models.DebugTalk.filter(project_id=api.project_id).first()

        variables = await models.Variables.filter(project_id=api.project_id).values("key", "value")

        config_body = {} if self.request.args.get("config") == "请选择" else eval(config.body)

        data = {
            "project_mapping": {
                "PWD": "",
                "functions": {},
                "env": {}
            },
            "testcases": []
        }

        test_struct = {
            "config": config_body,
            "teststeps": [eval(api.body)]
        }

        data["testcases"].append(test_struct)

        runner = HttpRunner(failfast=False)
        runner.run(data)

        summary = runner.summary

        result = {
            "name": summary["time"]["start_datetime"],
            "type": 1,
            "summary": [summary],
            "project": pro
        }
        await models.Report.create(**result)

        return resp_json(msg="报告添加成功!")


class RunApiTreeView(GenericAPIView):
    """
    运行api  tree
    """
    async def post(self, request):
        host = await models.HostIP.filter(name=request.json.get("host")).first()
        config = await models.Config.filter(name=request.json.get("config")).first()
        name = request.json.get("name")
        back_async = request.json.get("async")
        relation = request.json.get("relation")
        pro = await models.Project.filter(pk=request.json.get("project")).first()

        config_body = {} if request.json.get("config") == "请选择" else eval(config.body)

        test_case = []

        if host != "请选择":
            host = await models.HostIP.get(name=host, project=pro)
        for relation_id in relation:
            api = await models.API.filter(project=request.json.get("project"), relation=relation_id).order_by("id").values("body")

            for content in api:
                api = eval(content['body'])

        data = {
            "project_mapping": {
                "PWD": "",
                "functions": {},
                "env": {}
            },
            "testcases": []
        }

        test_struct = {
            "config": config_body,
            "teststeps": [api]
        }

        data["testcases"].append(test_struct)

        runner = HttpRunner(failfast=False)
        runner.run(data)

        if back_async:
            summary = loader.TEST_NOT_EXISTS
            summary["msg"] = "接口运行中，请稍后查看报告"
        else:
            summary = runner.summary
        result = {
            "name": summary["time"]["start_datetime"],
            "type": 1,
            "summary": [summary],
            "project": pro
        }
        await models.Report.create(**result)

        return resp_json(msg="报告添加成功!")


class RunView(GenericAPIView):
    """
    运行api
    """
    async def post(self, request):

        host = await models.HostIP.filter(name=request.json.get("host")).first()
        config_body = await models.Config.filter(name=request.json.get("config")).first()

        pro = await models.Project.filter(pk=request.json.get("project")).first()

        config = {} if request.json.get("config") == "请选择" else eval(config_body.body)

        test_config = {
            "name": request.json.get("name"),
            "request": {
                "url": request.json.get("url"),
                "method": request.json.get("method"),
                "headers": request.json.get("header")["header"],
                "form": request.json.get("request")["form"]["data"],
                "json": request.json.get("request")["json"],
                "params": request.json.get("request")["params"]["params"],
            },
            "extract": request.json.get("extract")["extract"],
            "validate": request.json.get("validate")["validate"],
            "setup_hooks": request.json.get("hooks")["setup_hooks"],
            "teardown_hooks": request.json.get("hooks")["teardown_hooks"],
        }

        test_case = {
            "name": request.json.get("name"),
            "body": test_config,
            "url": request.json.get("url"),
            "method": request.json.get("method"),
            "relation": request.json.get("nodeId"),
            "project": pro,
        }

        data = {
            "project_mapping": {
                "PWD": "",
                "functions": {},
                "env": {}
            },
            "testcases": []
        }

        test_struct = {
            "config": config,
            "teststeps": [test_case]
        }

        data["testcases"].append(test_struct)

        runner = HttpRunner(failfast=False)
        runner.run(data)
        summary = runner.summary

        result = {
            "name": summary["time"]["start_datetime"],
            "type": 1,
            "summary": [summary],
            "project": pro
        }
        await models.Report.create(**result)

        return resp_json(msg="报告添加成功!")


class RunSuiteTreeView(GenericAPIView):
    """
    运行测试用例树
    """
    async def post(self, request):

        host = await models.HostIP.filter(name=request.json.get("host")).first()
        name = request.json.get("name")
        back_async = request.json.get("async")
        relation = request.json.get("relation")
        pro = await models.Project.filter(pk=request.json.get("project")).first()

        test_sets = []
        suite_list = []
        config_list = []

        if host != "请选择":
            host = await models.HostIP.get(name=host, project=pro)
        for relation_id in relation:
            suite = await models.Case.filter(project=request.json.get("project"), relation=relation_id).order_by(
                "id").values("id", "name")

            for content in suite:
                test_list = await models.CaseStep.filter(case_id=content["id"]).order_by("step").values("body")
                testcase_list = []
                config = {}
                for content in test_list:
                    body = eval(content['body'])

                    if "base_url" in body["request"]:
                        config = await models.Config.filter(name=body["name"], project=request.json.get("project"))
                        continue
                    testcase_list.append(parse_host(host, body))

                config_list.append(parse_host(host, config))
                test_sets.append(testcase_list)
                suite_list += suite

        data = {
            "project_mapping": {
                "PWD": "",
                "functions": {},
                "env": {}
            },
            "testcases": []
        }

        test_struct = {
            "config": config,
            "teststeps": suite_list
        }

        data["testcases"].append(test_struct)

        runner = HttpRunner(failfast=False)
        runner.run(data)

        if back_async:
            summary = loader.TEST_NOT_EXISTS
            summary["msg"] = "接口运行中，请稍后查看报告"
        else:
            summary = runner.summary

        result = {
            "name": summary["time"]["start_datetime"],
            "type": 1,
            "summary": [summary],
            "project": pro
        }
        await models.Report.create(**result)

        return resp_json(msg="报告添加成功!")


class RunTestView(GenericAPIView):
    """
    运行test by id
    """
    async def get(self, request):
        host = await models.HostIP.filter(name=self.request.args.get("host")).first()
        name = self.request.args.get("name")
        pro = self.request.args.get("project")

        test_list = await models.CaseStep.filter(case_id__in=self.request.args.get("id")).order_by("step").values("body")

        test_case = []
        config = {}
        if host != "请选择":
            host = await models.HostIP.filter(name=host, project=pro)

        for content in test_list:

            body = eval(content["body"])
            if "base_url" in body["request"]:
                config = await models.Config.filter(name=body["name"], project=request.json.get("project"))
                continue
            test_case.append(parse_host(host, body))

        data = {
            "project_mapping": {
                "PWD": "",
                "functions": {},
                "env": {}
            },
            "testcases": []
        }

        test_struct = {
            "config": config,
            "teststeps": test_case
        }

        data["testcases"].append(test_struct)

        runner = HttpRunner(failfast=False)
        runner.run(data)

        summary = runner.summary

        result = {
            "name": summary["time"]["start_datetime"],
            "type": 1,
            "summary": [summary],
            "project": pro
        }
        await models.Report.create(**result)

        return resp_json(msg="报告添加成功!")


bp.add_route(RunTestView.as_view(), '/run_testsuite_pk/')

bp.add_route(RunSuiteTreeView.as_view(), '/run_suite_tree/')

bp.add_route(RunView.as_view(), '/run_api/')

bp.add_route(RunApiTreeView.as_view(), '/run_api_tree/')

bp.add_route(RunApiView.as_view(), '/run_api_pk/')
