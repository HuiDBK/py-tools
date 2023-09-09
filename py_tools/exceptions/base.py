#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/02/12 22:09
from py_tools.enums.error import BaseErrCodeEnum


class CommonException(Exception):
    """通用异常"""
    pass


class BizException(CommonException):
    """业务异常"""

    def __init__(
            self,
            msg: str = "",
            code: str = BaseErrCodeEnum.FAILED.value,
            err_enum: BaseErrCodeEnum = None
    ):
        self.code = code
        self.msg = msg

        if err_enum:
            self.code = err_enum.code
            self.msg = self.msg or err_enum.msg


class MaxRetryException(BizException):
    """最大重试次数异常"""

    def __init__(self, msg: str = BaseErrCodeEnum.FUNC_TIMEOUT_ERR.msg):
        super().__init__(msg=msg, err_enum=BaseErrCodeEnum.FUNC_RETRY_ERR)


class MaxTimeoutException(BizException):
    """最大超时异常"""

    def __init__(self, msg: str = BaseErrCodeEnum.FUNC_TIMEOUT_ERR.msg):
        super().__init__(msg=msg, err_enum=BaseErrCodeEnum.FUNC_TIMEOUT_ERR)


class SendMsgException(BizException):
    """发送消息异常"""
    pass
