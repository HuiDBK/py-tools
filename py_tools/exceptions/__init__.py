#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 自定义异常包 }
# @Date: 2023/02/12 22:07
from py_tools.exceptions.base import (
    MaxTimeoutException,
    SendMsgException,
    MaxRetryException,
    BizException,
    CommonException,
)

__all__ = ["MaxTimeoutException", "SendMsgException", "MaxRetryException", "BizException", "CommonException"]
