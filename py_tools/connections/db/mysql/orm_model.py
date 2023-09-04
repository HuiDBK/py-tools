#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/08/17 23:55
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseOrmTable(AsyncAttrs, DeclarativeBase):
    """SQLAlchemy Base ORM Model"""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, comment="主键ID")

    created_at: Mapped[datetime] = mapped_column(default=func.now, comment="创建时间")

    updated_at: Mapped[datetime] = mapped_column(default=func.now, onupdate=func.now, comment="更新时间")

    deleted_at: Mapped[datetime] = mapped_column(nullable=True, comment="删除时间")

    def to_dict(self, alias_dict: dict = None, exclude_none=True) -> dict:
        """
        数据库模型转成字典
        Args:
            alias_dict: 字段别名字典
                eg: {"id": "user_id"}, 把id名称替换成 user_id
            exclude_none: 默认排查None值
        Returns: dict
        """
        if exclude_none:
            return {
                alias_dict.get(c.name, c.name): getattr(self, c.name)
                for c in self.__table__.columns if getattr(self, c.name) is not None
            }
        else:
            return {
                alias_dict.get(c.name, c.name): getattr(self, c.name, None)
                for c in self.__table__.columns
            }
