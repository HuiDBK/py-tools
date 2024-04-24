#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 公用业务枚举 }
# @Date: 2023/09/09 23:54
from py_tools.enums import BaseEnum


class SwitchEnum(BaseEnum):
    """开关枚举"""
    OFF = 0  # 关
    ON = 1  # 开


class YesNoEnum(BaseEnum):
    """开关枚举"""
    NO = 0  # 否
    YES = 1  # 是


class RedisTypeEnum(BaseEnum):
    """Redis 数据类型"""

    String = "String"
    List = "List"
    Hash = "Hash"
    Set = "Set"
    ZSet = "ZSet"
