#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/3  下午4:53

import datetime

from sanic.exceptions import abort

from tortoise import fields
from tortoise.models import Model
from tortoise.models import ModelMeta as _ModelMeta


BASE_APP_NAME = 'Api'


class ModelMeta(_ModelMeta):
    """
    此处可以作一些自由的封装
    """
    ...


class BaseModel(Model, metaclass=ModelMeta):
    """
    重新定制 `Model`
    """
    id = fields.IntField(pk=True)
    create_time = fields.DatetimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = fields.DatetimeField(auto_now=True, verbose_name="更新时间")

    @property
    def pk(self):
        return self.id

    @classmethod
    async def get_or_404(cls, pk):
        # TODO 支持更多的过滤条件
        instance = await cls.filter(id=pk).first()
        # 如果获取到没有
        if not instance:
            abort(404)

        return instance

    async def save(self, *args, **kwargs):
        # FIXME 遗留问题, ORM不具备时区支持, 重写 `save` 方法, 后续改进
        # 修改时间时区
        for field, field_type in self._meta.fields_map.items():
            # 如果不是时间字段, 继续上层循环
            if not isinstance(field_type, fields.DatetimeField):
                continue

            # 首次添加操作, 每个都进行设置
            if not self.id and field_type.auto_now_add:
                setattr(self, field, datetime.datetime.now())

            # 如果是更新, `auto_now` 表示每次操作表示更新, 否则不更新
            if self.id and field_type.auto_now:
                setattr(self, field, datetime.datetime.now())

        await super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class ContentType(BaseModel):
    """
    此表摘自于 `django`
    """
    app_label = fields.CharField(max_length=128)
    model = fields.CharField(max_length=128)

    class Meta:
        table = "django_content_type"


class UserInfo(BaseModel):
    """
    用户信息
    """
    username = fields.CharField(verbose_name="用户名", max_length=64)
    password = fields.CharField(verbose_name="密码", max_length=125)

    def __str__(self):
        return self.username

    class Meta:
        table = f'{BASE_APP_NAME}_UserInfo'


class Project(BaseModel):
    """
    项目信息表
    """
    name = fields.CharField(verbose_name="项目名", max_length=64)
    desc = fields.CharField(verbose_name="描述", max_length=125)
    responsible = fields.CharField(verbose_name="项目负责人", max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        table = f"{BASE_APP_NAME}_Project"


class DebugTalk(BaseModel):
    """
    驱动表
    """
    code = fields.TextField(default="# Write you code", verbose_name="Python代码", null=False)
    project = fields.ForeignKeyField("models.Project", unique=True, verbose_name="对应项目")

    def __str__(self):
        return self.code

    class Meta:
        table = f"{BASE_APP_NAME}_DebugTalk"


class Config(BaseModel):
    """
    环境配置表
    """
    name = fields.CharField(verbose_name="环境名称", max_length=100)
    body = fields.TextField(verbose_name="信息描述")
    base_url = fields.CharField(verbose_name="请求地址", max_length=100)
    project = fields.ForeignKeyField("models.Project", verbose_name="对应项目")

    def __str__(self):
        return self.name

    class Meta:
        table = f"{BASE_APP_NAME}_Config"


class API(BaseModel):
    """
    API 信息表
    """
    name = fields.CharField(verbose_name="接口名称", max_length=100)
    body = fields.TextField(verbose_name="信息描述")
    url = fields.CharField(verbose_name="请求地址", max_length=100)
    method = fields.CharField(verbose_name="请求方式", max_length=100)
    relation = fields.IntField(verbose_name="节点ID")
    project = fields.ForeignKeyField("models.Project", verbose_name="对应项目")

    def __str__(self):
        return self.name

    class Meta:
        table = f"{BASE_APP_NAME}_API"


class Case(BaseModel):
    """
    测试用例信息表
    """
    tag_types = (
        (1, "冒烟测试"),
        (2, "集成测试"),
        (3, "监控脚本"),
    )
    name = fields.CharField(verbose_name="用例名字", max_length=100)
    tag = fields.IntField(verbose_name="用例标签", choices=tag_types)
    count = fields.IntField(verbose_name="API数量")
    relation = fields.IntField(verbose_name="节点ID")
    project = fields.ForeignKeyField('models.Project')

    def __str__(self):
        return self.name

    class Meta:
        table = f"{BASE_APP_NAME}_Case"


class CaseStep(BaseModel):
    """
    测试用例步骤
    """
    name = fields.CharField(verbose_name="用例名字", max_length=100)
    body = fields.TextField(verbose_name="信息描述")
    url = fields.CharField(verbose_name="请求地址", max_length=100)
    method = fields.CharField(verbose_name="请求方式", max_length=100)
    step = fields.IntField(verbose_name="顺序")
    case = fields.ForeignKeyField("models.Case")

    def __str__(self):
        return self.name

    class Meta:
        table = f"{BASE_APP_NAME}_CaseStep"


class HostIP(BaseModel):
    """
    主机配置
    """
    name = fields.CharField(verbose_name="用例名字", max_length=100)
    value = fields.TextField(verbose_name="信息描述")
    project = fields.ForeignKeyField("models.Project")

    def __str__(self):
        return self.name

    class Meta:
        table = f"{BASE_APP_NAME}_HostIP"


class Variables(BaseModel):
    """
    全局变量
    """
    key = fields.CharField(verbose_name="变量Key", max_length=100)
    value = fields.CharField(verbose_name="变量Value", max_length=100)
    project = fields.ForeignKeyField("models.Project")

    def __str__(self):
        return self.name

    class Meta:
        table = f"{BASE_APP_NAME}_Variables"


class Report(BaseModel):
    """
    测试报告
    """
    report_type = (
        (1, "调试用例报告"),
        (2, "异步任务报告"),
        (3, "定时任务报告"),
    )

    name = fields.CharField(verbose_name="报告名", max_length=100)
    type = fields.IntField(choices=report_type, verbose_name="报告类型")
    summary = fields.TextField(verbose_name="报告描述")
    project = fields.ForeignKeyField("models.Project")

    def __str__(self):
        return self.name

    class Meta:
        table = f"{BASE_APP_NAME}_Report"


class Relation(BaseModel):
    """
    树形结构关系
    """
    project = fields.ForeignKeyField("models.Project")
    tree = fields.TextField(verbose_name="关系主题")
    type = fields.IntField(verbose_name="树类型", default=1)

    def __str__(self):
        return self.name

    class Meta:
        table = f"{BASE_APP_NAME}_Relation"
