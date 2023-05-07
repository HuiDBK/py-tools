#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 飞书相关枚举 }
# @Date: 2023/05/03 18:52
from py_tools.enums.base import BaseEnum


class FeishuReceiveType(BaseEnum):
    """消息接收者id类型"""

    OPEN_ID = "open_id"  # 标识一个用户在某个应用中的身份
    USER_ID = "user_id"  # 标识一个用户在某个租户内的身份
    UNION_ID = "union_id"  # 标识一个用户在某个应用开发商下的身份
    EMAIL = "email"  # 以用户的真实邮箱来标识用户
    CHAT_ID = "chat_id"  # 以群ID来标识群聊
