#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/08/17 23:55
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseOrmTable(AsyncAttrs, DeclarativeBase):
    """SQLAlchemy Base ORM Model"""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-1, comment="主键ID")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.to_dict()}>"

    @classmethod
    def all_columns(cls):
        return [column for column in cls.__table__.columns]

    def to_dict(self, alias_dict: dict = None, exclude_none=False) -> dict:
        """
        数据库模型转成字典
        Args:
            alias_dict: 字段别名字典
                eg: {"id": "user_id"}, 把id名称替换成 user_id
            exclude_none: 默认排查None值
        Returns: dict
        """
        alias_dict = alias_dict or {}
        if exclude_none:
            return {
                alias_dict.get(c.name, c.name): getattr(self, c.name)
                for c in self.all_columns()
                if getattr(self, c.name) is not None
            }
        else:
            return {alias_dict.get(c.name, c.name): getattr(self, c.name) for c in self.all_columns()}


class TimestampColumns(AsyncAttrs, DeclarativeBase):
    """时间戳相关列"""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, comment="创建时间")

    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, comment="更新时间")

    deleted_at: Mapped[datetime] = mapped_column(nullable=True, comment="删除时间")


class BaseOrmTableWithTS(BaseOrmTable, TimestampColumns):
    __abstract__ = True
