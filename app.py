#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/3  下午2:16

import os

import asyncio

import logging
from initial import init_db
from config import config_info
from werkzeug.utils import find_modules, import_string
from sanic import Sanic


def register_blueprints(root, _app):
    """注册蓝图

    """
    for name in find_modules(root, recursive=True):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            _app.register_blueprint(mod.bp)


app = Sanic()


@app.listener('before_server_start')
async def setup_db(_, loop):
    # 设置任务工厂
    # 初始化db
    await init_db()


app.config.update(config_info['DATABASES'])
register_blueprints('api', app)


if __name__ == '__main__':
    app.run(**config_info['run_info'])
