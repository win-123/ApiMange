#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/4  下午6:42

import hashlib
import time


def generate_token(username):
    """
    生成token
    :param username:
    :return:
    """
    timestamp = str(time.time())

    token = hashlib.md5(bytes(username, encoding='utf-8'))
    token.update(bytes(timestamp, encoding='utf-8'))

    return token.hexdigest()
