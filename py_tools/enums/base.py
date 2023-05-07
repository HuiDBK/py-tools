#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/04/30 20:54
from enum import Enum


class BaseEnum(Enum):
    """枚举基类"""

    def __new__(cls, value, desc=None):
        """
        构造枚举成员实例
        Args:
            value: 枚举成员的值
            desc: 枚举成员的描述信息，默认None
        """
        obj = object.__new__(cls)
        obj._value_ = value
        obj.desc = desc
        return obj

    @classmethod
    def get_members(cls, exclude_enums: list = None, only_value: bool = False) -> list:
        """
        获取枚举的所有成员
        Args:
            exclude_enums: 排除的枚举类列表
            only_value: 是否只需要成员的值，默认False

        Returns: 枚举成员列表 or 枚举成员值列表

        """
        members = list(cls)
        if exclude_enums:
            # 排除指定枚举
            members = [member for member in members if member not in exclude_enums]

        if only_value:
            # 只需要成员的值
            members = [member.value for member in members]

        return members

    @classmethod
    def get_values(cls, exclude_enums: list = None):
        return cls.get_members(exclude_enums=exclude_enums, only_value=True)

    @classmethod
    def get_names(cls):
        return list(cls._member_names_)


class StrEnum(str, BaseEnum):
    """字符串枚举"""


class IntEnum(int, BaseEnum):
    """整型枚举"""
