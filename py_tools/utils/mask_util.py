#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 字符串掩码工具类模块 }
# @Date: 2022/11/26 18:09
import re
from typing import Union


class MaskUtil(object):
    """掩码工具类"""

    # 元素掩码的格式 (匹配规则, 替换后的内容)
    # \1, \3 指的是取第几个分组数据相当于 group(1)、group(3)
    ADDRESS = (r"(\w)", r"*")  # 地址
    NAME = (r"(.{1})(.{1})(.*)", r"\1*\3")  # 名字
    PHONE = (r"(\d{3})(.*)(\d{4})", r"\1****\3")  # 电话号码
    ID_CARD = (r"(\d{6})(.*)(\d{4})", r"\1****\3")  # 身份证
    WECHAT_NUM = (r"(.{1})(.*)(.{1})", r"\1****\3")  # 微信号

    @classmethod
    def mask(cls, origin_text: str, mask_type: Union[tuple, str] = NAME):
        """数据掩码"""
        if isinstance(mask_type, tuple):
            return re.sub(*mask_type, str(origin_text))
        elif isinstance(mask_type, str):
            mark_rule_tuple = getattr(cls, mask_type.upper())
            return cls.mask(origin_text, mark_rule_tuple)
        return origin_text

    @classmethod
    def mask_phone(cls, origin_text: str, mask_type: Union[tuple, str] = PHONE):
        return cls.mask(origin_text, mask_type)
