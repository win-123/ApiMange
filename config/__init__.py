#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/3  下午2:13

import sys
from config.conf import dev, prod

config_info = {}


def init():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return 'dev'


profile = init()

if 'dev' == profile:
    config_info = dev
elif 'prod' == profile:
    config_info = prod
