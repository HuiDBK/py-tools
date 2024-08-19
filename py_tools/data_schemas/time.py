#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 时间数据模型 }
# @Date: 2023/04/30 23:35
from pydantic import BaseModel


class DateDiff(BaseModel):
    years: int
    months: int
    days: int
    hours: int
    minutes: int
    seconds: int
