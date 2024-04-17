#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { sqlalchemy demo }
# @Date: 2023/09/04 14:22
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from py_tools.connections.db.mysql import BaseOrmTable, BaseOrmTableWithTS


class UserTable(BaseOrmTableWithTS):
    """用户表"""

    __tablename__ = "user"
    username: Mapped[str] = mapped_column(default="", comment="用户昵称")
    age: Mapped[int] = mapped_column(default=0, comment="年龄")
    password: Mapped[str] = mapped_column(default="", comment="用户密码")
    phone: Mapped[str] = mapped_column(default="", comment="手机号")
    email: Mapped[str] = mapped_column(default="", comment="邮箱")
    avatar: Mapped[str] = mapped_column(default="", comment="头像")


class UserFileTable(BaseOrmTable):
    """用户文件表"""

    __tablename__ = "user_file"
    filename: Mapped[str] = mapped_column(String(100), default="", comment="文件名称")
    creator: Mapped[int] = mapped_column(default=0, comment="文件创建者")
    file_suffix: Mapped[str] = mapped_column(String(100), default="", comment="文件后缀")
    file_size: Mapped[int] = mapped_column(default=0, comment="文件大小")
    oss_key: Mapped[str] = mapped_column(String(100), default="", comment="oss key（minio）")
    is_del: Mapped[int] = mapped_column(default=0, comment="是否删除")
    deleted_at: Mapped[datetime] = mapped_column(nullable=True, comment="删除时间")
