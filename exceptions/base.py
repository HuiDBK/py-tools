#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/02/12 22:09


class BusinessException(Exception):
    """业务异常通用"""
    pass


class MaxRetryException(BusinessException):
    """最大重试次数异常"""
    pass


class MaxTimeoutException(BusinessException):
    """最大超时异常"""
    pass


class SendMsgException(BusinessException):
    """发送消息异常"""
    pass
