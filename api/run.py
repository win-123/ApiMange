#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/22  下午2:58

from schema import project
from sanic import Blueprint
from core.response import resp_json
from utils import loader
from core.status import FAIL
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

        debug_talk = await models.DebugTalk.filter(project_id=api.project_id).first()

        variables = await models.Variables.filter(project_id=api.project_id).values("key", "value")

        config_body = None if self.request.args.get("config") == "请选择" else eval(config.body)

        summary = loader.debug_api(eval(api.body), debug_talk.code, variables, config=config_body )

        return resp_json()


bp.add_route(RunApiView.as_view(), '/run_api_pk/')
