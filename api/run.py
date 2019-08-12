#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/22  下午2:58

from schema import project
from sanic import Blueprint
from core.response import resp_json
from utils import loader
from core.status import FAIL
from httprunner.api import HttpRunner
import models

from .base import GenericAPIView

bp = Blueprint('run', url_prefix='/api')


class RunApiView(GenericAPIView):
    """
    运行api
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


bp.add_route(RunApiView.as_view(), '/run_api_pk/')
