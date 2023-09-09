#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 错误码枚举 }
# @Date: 2023/09/09 14:45
from py_tools.enums import StrEnum


class BaseErrCodeEnum(StrEnum):
    """
    错误码前缀
     - 000-通用基础错误码前缀
     - 100-待定
     - 200-通用业务错误码前缀
        eg:
        - 201-用户模块
        - 202-订单模块
     - 300-待定
     - 400-通用请求错误
     - 500-通用系统错误码前缀
    """
    OK = ("000-0000", "SUCCESS")
    FAILED = ("000-0001", "FAILED")
    FUNC_TIMEOUT_ERR = ("000-0002", "函数最大超时错误")
    FUNC_RETRY_ERR = ("000-0003", "函数最大重试错误")
    SEND_SMS_ERR = ("000-0004", "发送短信错误")
    SEND_EMAIL_ERR = ("000-0005", "发送邮件错误")

    AUTH_ERR = ("400-0401", "权限认证错误")
    LOGIN_ERR = ("400-0403", "未登陆错误")
    NOT_FOUND_ERR = ("400-0404", "未找到资源错误")
    PARAM_ERR = ("400-0422", "参数错误")

    SYSTEM_ERR = ("500-0500", "系统异常")
    SOCKET_ERR = ("500-0501", "网络异常")
    GATEWAY_ERR = ("500-0502", "网关异常")

    @property
    def code(self):
        return self.value

    @property
    def msg(self):
        return self.desc
