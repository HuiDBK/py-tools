#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/02/12 21:38
from enum import Enum


class TimeFormatEnum(Enum):
    """时间格式化枚举"""
    DateTime = "%Y-%m-%d %H:%M:%S"
    DateOnly = "%Y-%m-%d"
    TimeOnly = "%H:%M:%S"
