#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { http相关枚举 }
# @Date: 2023/08/10 09:37

from py_tools.enums.base import BaseEnum


class HttpMethod(BaseEnum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
