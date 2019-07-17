#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/5  上午9:56

from marshmallow import fields
from .base import BasicSchema


class LoginSchema(BasicSchema):
    """
    变量
    """
    username = fields.String()
    password = fields.String()


class RegisterSchema(BasicSchema):
    """
    变量
    """
    username = fields.String()
    password = fields.String()
    email = fields.String()
