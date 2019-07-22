#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/22  下午2:58

from schema import project
from sanic import Blueprint
from core.response import resp_json
from core.status import FAIL
import models

from .base import GenericAPIView

bp = Blueprint('run', url_prefix='/api')


class RunApiView(GenericAPIView):
    """
    运行api
    """
    async def get(self, request):
        return resp_json()



bp.add_route(RunApiView.as_view(), '/run_api_pk/')
