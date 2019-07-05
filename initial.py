#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/4  下午5:40

from tortoise import Tortoise

from config import config_info


async def init_db(create_db=False):
    """
    init 数据
    :param create_db:
    :return:
    """
    await Tortoise.init(
        {
            "connections": config_info["DATABASES"],
            "apps": {
                "models": {
                    "models": ["models"],
                    "default_connection": "default"
                }
            },
        },
        _create_db=create_db
    )
