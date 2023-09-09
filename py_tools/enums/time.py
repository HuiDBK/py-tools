#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/02/12 21:38
from py_tools.enums.base import StrEnum


class TimeFormatEnum(StrEnum):
    """时间格式化枚举"""
    DateTime = "%Y-%m-%d %H:%M:%S"
    DateOnly = "%Y-%m-%d"
    TimeOnly = "%H:%M:%S"

    DateTime_CN = "%Y年%m月%d日 %H时%M分%S秒"
    DateOnly_CN = "%Y年%m月%d日"
    TimeOnly_CN = "%H时%M分%S秒"


class TimeUnitEnum(StrEnum):
    """时间单位枚举"""
    DAYS = "days"
    HOURS = "hours"
    MINUTES = "minutes"
    SECONDS = "seconds"
