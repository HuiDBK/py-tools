#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/08/17 23:57
import logging
from datetime import datetime
from typing import Type, Any, Union, List
from loguru import logger
from sqlalchemy import update, delete, insert

from orm_model import BaseOrmTable
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine


class SQLAIChemyManager:
    DB_URL_TEMPLATE = "{protocol}://{user}:{password}@{host}:{port}/{db}"

    def __init__(
            self,
            host: str = "localhost",
            port: int = 3306,
            user: str = "",
            password: str = "",
            db_name: str = "",
            pool_size: int = 30,
            pool_pre_ping: bool = True,
            pool_recycle: int = 600,
            log: Union[logging.Logger, logger] = None
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.pool_size = pool_size
        self.pool_pre_ping = pool_pre_ping
        self.pool_recycle = pool_recycle
        self.log = log or logger

        self.db_engine: AsyncEngine = None
        self.async_session_maker: async_sessionmaker = None

    def get_db_url(self, protocol: str = "mysql+aiomysql"):
        db_url = self.DB_URL_TEMPLATE.format(
            protocol=protocol,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            db=self.db_name
        )
        return db_url

    def init_mysql_engine(self, protocol: str = "mysql+aiomysql"):
        """
        初始化mysql引擎
        Args:
            protocol: 驱动协议类型

        Returns:
            self.db_engine
        """
        db_url = self.get_db_url(protocol=protocol)
        self.log.info(f"init_mysql_engine => {db_url}")
        self.db_engine = create_async_engine(
            url=db_url,
            pool_size=self.pool_size,
            pool_pre_ping=self.pool_pre_ping,
            pool_recycle=self.pool_recycle
        )
        self.async_session_maker = async_sessionmaker(bind=self.db_engine, expire_on_commit=False)
        return self.db_engine

    async def batch_delete_by_ids(
            self,
            orm_table: Type[BaseOrmTable],
            pk_ids: list,
            logic_del: bool = False,
            logic_field: str = "deleted_at",
            logic_del_set_value: Any = None,
    ):
        """
        根据主键id批量删除
        Args:
            orm_table: 数据库表orm table
            pk_ids: 主键id列表
            logic_del: 逻辑删除，默认 False 物理删除 True 逻辑删除
            logic_field: 逻辑删除字段 默认 deleted_at
            logic_del_set_value: 逻辑删除字段设置的值

        Returns: 删除的记录数
        """
        async with self.async_session_maker() as session:
            # 构建删除条件
            delete_condition = orm_table.id.in_(pk_ids)

            if logic_del:
                # 执行逻辑删除操作
                logic_del_info = dict()
                logic_del_info[logic_field] = logic_del_set_value or datetime.now()
                delete_stmt = update(orm_table).where(delete_condition).values(**logic_del_info)
            else:
                # 执行物理删除操作
                delete_stmt = delete(orm_table).where(delete_condition)

            result = await session.execute(delete_stmt)
            await session.commit()

            # 返回影响的记录数
            return result.rowcount

    async def bulk_insert(self, table: Type[BaseOrmTable], data_list: List[dict]):
        """
        批量插入
        Args:
            table: 数据表实例
            data_list: 数据集

        Returns:
            成功插入的影响行数
        """
        async with self.async_session_maker() as session:
            sql = insert(table).values(data_list)
            result = await session.execute(sql)
            await session.commit()
            return result.rowcount
