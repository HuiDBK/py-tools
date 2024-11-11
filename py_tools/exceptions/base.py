#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/02/12 22:09
from py_tools.enums.error import BaseErrCode, BaseErrCodeEnum


class CommonException(Exception):
    """通用异常"""

    pass


class BizException(CommonException):
    """业务异常"""

    def __init__(self, msg: str = "", code: str = BaseErrCodeEnum.FAILED.code, err_code: BaseErrCode = None):
        self.code = code
        self.msg = msg

        if err_code:
            self.code = err_code.code
            self.msg = self.msg or err_code.msg


class MaxRetryException(BizException):
    """最大重试次数异常"""

    def __init__(self, msg: str = BaseErrCodeEnum.FUNC_TIMEOUT_ERR.msg):
        super().__init__(msg=msg, err_code=BaseErrCodeEnum.FUNC_RETRY_ERR)


class MaxTimeoutException(BizException):
    """最大超时异常"""

    def __init__(self, msg: str = BaseErrCodeEnum.FUNC_TIMEOUT_ERR.msg):
        super().__init__(msg=msg, err_code=BaseErrCodeEnum.FUNC_TIMEOUT_ERR)


class SendMsgException(BizException):
    """发送消息异常"""

    pass
