#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/02/12 21:38
from py_tools.enums.base import BaseEnum


class TimeFormatEnum(BaseEnum):
    """时间格式化枚举"""
    DateTime = "%Y-%m-%d %H:%M:%S"
    DateOnly = "%Y-%m-%d"
    TimeOnly = "%H:%M:%S"


class TimeUnitEnum(BaseEnum):
    """时间单位枚举"""
    DAYS = "days"
    HOURS = "hours"
    MINUTES = "minutes"
    SECONDS = "seconds"
