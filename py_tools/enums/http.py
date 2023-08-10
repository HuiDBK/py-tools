#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { http相关枚举 }
# @Date: 2023/08/10 09:37
from py_tools.enums import BaseEnum


class HttpMethod(BaseEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class RespFmt(BaseEnum):
    """http响应格式"""
    JSON = "json"
    BYTES = "bytes"
    TEXT = "text"
