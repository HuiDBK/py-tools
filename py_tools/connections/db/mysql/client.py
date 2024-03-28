#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 数据库连接客户端模块 }
# @Date: 2023/08/17 23:57
import asyncio
import functools
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Type, Any, Union, List, TypeVar
from loguru import logger
from sqlalchemy import update, delete, insert, text, select, func, column, Result

from py_tools.connections.db.mysql import BaseOrmTable
from py_tools.meta_cls import SingletonMetaCls
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

T_BaseOrmTable = TypeVar('T_BaseOrmTable', bound=BaseOrmTable)
T_Hints = TypeVar("T_Hints")  # 用于修复被装饰的函数参数提示，让IDE有类型提示


def with_session(method) -> T_Hints:
    """
    兼容事务
    Args:
        method: orm 的 crud

    Notes:
        方法中没有带事务连接则，则构造

    Returns:
    """

    @functools.wraps(method)
    async def wrapper(db_manager, *args, **kwargs):
        session = kwargs.get("session") or None
        if session:
            return await method(db_manager, *args, **kwargs)
        else:
            async with db_manager.transaction() as session:
                kwargs["session"] = session
                return await method(db_manager, *args, **kwargs)

    return wrapper


class SQLAlchemyManager(metaclass=SingletonMetaCls):
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
            log: Union[logging.Logger] = None
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


class DBManager(metaclass=SingletonMetaCls):
    DB_CLIENT: SQLAlchemyManager = None
    orm_table: Type[BaseOrmTable] = None

    @classmethod
    def init_db_client(cls, db_client: SQLAlchemyManager):
        cls.DB_CLIENT = db_client
        return cls.DB_CLIENT

    @classmethod
    @asynccontextmanager
    async def transaction(cls):
        """事务上下文管理器"""
        async with cls.DB_CLIENT.async_session_maker.begin() as session:
            yield session

    @with_session
    async def bulk_delete_by_ids(
            self,
            pk_ids: list,
            orm_table: Type[BaseOrmTable] = None,
            logic_del: bool = False,
            logic_field: str = "deleted_at",
            logic_del_set_value: Any = None,
            session: AsyncSession = None
    ):
        """
        根据主键id批量删除
        Args:
            pk_ids: 主键id列表
            orm_table: orm表映射类
            logic_del: 逻辑删除，默认 False 物理删除 True 逻辑删除
            logic_field: 逻辑删除字段 默认 deleted_at
            logic_del_set_value: 逻辑删除字段设置的值
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns: 删除的记录数
        """
        orm_table = orm_table or self.orm_table
        conds = [orm_table.id.in_(pk_ids)]
        return await self.delete(
            conds=conds,
            orm_table=orm_table,
            logic_del=logic_del,
            logic_field=logic_field,
            logic_del_set_value=logic_del_set_value,
            session=session
        )

    @with_session
    async def delete_by_id(
            self,
            pk_id: int,
            orm_table: Type[BaseOrmTable] = None,
            logic_del: bool = False,
            logic_field: str = "deleted_at",
            logic_del_set_value: Any = None,
            session: AsyncSession = None
    ):
        """
        根据主键id删除
        Args:
            pk_id: 主键id
            orm_table: orm表映射类
            logic_del: 逻辑删除，默认 False 物理删除 True 逻辑删除
            logic_field: 逻辑删除字段 默认 deleted_at
            logic_del_set_value: 逻辑删除字段设置的值
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns: 删除的记录数
        """
        orm_table = orm_table or self.orm_table
        conds = [orm_table.id == pk_id]
        return await self.delete(
            conds=conds,
            orm_table=orm_table,
            logic_del=logic_del,
            logic_field=logic_field,
            logic_del_set_value=logic_del_set_value,
            session=session
        )

    @with_session
    async def delete(
            self,
            conds: list = None,
            orm_table: Type[BaseOrmTable] = None,
            logic_del: bool = False,
            logic_field: str = "deleted_at",
            logic_del_set_value: Any = None,
            session: AsyncSession = None,
    ):
        """
        通用删除
        Args:
            conds: 条件列表, eg. [UserTable.id == 1]
            orm_table: orm表映射类
            logic_del: 逻辑删除，默认 False 物理删除 True 逻辑删除
            logic_field: 逻辑删除字段 默认 deleted_at
            logic_del_set_value: 逻辑删除字段设置的值
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns: 删除的记录数
        """
        orm_table = orm_table or self.orm_table

        if logic_del:
            # 执行逻辑删除操作
            logic_del_info = dict()
            logic_del_info[logic_field] = logic_del_set_value or datetime.now()
            delete_stmt = update(orm_table).where(*conds).values(**logic_del_info)
        else:
            # 执行物理删除操作
            delete_stmt = delete(orm_table).where(*conds)

        cursor_result = await session.execute(delete_stmt)

        # 返回影响的记录数
        return cursor_result.rowcount

    @with_session
    async def bulk_insert(
            self,
            add_rows: List[dict],
            orm_table: Type[BaseOrmTable] = None,
            session: AsyncSession = None,
    ) -> Union[int, Any]:
        """
        批量插入
        Args:
            orm_table: orm表映射类
            add_rows: 批量添加的数据集, eg. [{"username": "hui", "age": 18}, ...]
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns:
            成功插入的影响行数
        """
        orm_table = orm_table or self.orm_table
        sql = insert(orm_table).values(add_rows)
        result = await session.execute(sql)
        return result.rowcount

    @with_session
    async def bulk_add(self, table_objs: List[T_BaseOrmTable], session: AsyncSession = None) -> int:
        """
        批量插入
        Args:
            table_objs: orm映射类实例列表, eg. [UserTable(username="hui", age=18), ...]
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns:
            成功插入的影响行数
        """
        session.add_all(table_objs)
        return len(table_objs)

    @with_session
    async def add(self, table_obj: T_BaseOrmTable, session: AsyncSession = None) -> int:
        """
        插入一条数据
        Args:
            table_obj: orm映射类实例对象, eg. UserTable(username="hui", age=18)
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns: 新增的id
            table_obj.id
        """
        session.add(table_obj)
        return table_obj.id

    @with_session
    async def query_by_id(
            self,
            pk_id: int,
            orm_table: Type[BaseOrmTable] = None,
            session: AsyncSession = None,
    ) -> Union[T_BaseOrmTable, None]:
        """
        根据主键id查询
        Args:
            pk_id: 主键id
            orm_table: orm表映射类
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns:
            orm映射类的实例对象
        """
        orm_table = orm_table or self.orm_table
        ret = await session.get(orm_table, pk_id)
        return ret

    @with_session
    async def _query(
            self,
            cols: list = None,
            orm_table: BaseOrmTable = None,
            conds: list = None,
            orders: list = None,
            limit: int = None,
            offset: int = 0,
            session: AsyncSession = None,
    ) -> Result[Any]:
        """
        通用查询
        Args:
            cols: 查询的列表字段
            orm_table: orm表映射类
            conds: 查询的条件列表
            orders: 排序列表, 默认id升序
            limit: 限制数量大小
            offset: 偏移量
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns: 查询结果集
            cursor_result
        """
        cols = cols or []
        cols = [column(col_obj) if isinstance(col_obj, str) else col_obj for col_obj in cols]  # 兼容字符串列表

        conditions = conds or []
        orders = orders or [column("id")]
        orm_table = orm_table or self.orm_table

        # 构造查询
        if cols:
            # 查询指定列
            query_sql = select(*cols).select_from(orm_table).where(*conditions).order_by(*orders)
        else:
            # 查询全部字段
            query_sql = select(orm_table).where(*conditions).order_by(*orders)

        if limit:
            query_sql = query_sql.limit(limit).offset(offset)

        # 执行查询
        cursor_result = await session.execute(query_sql)
        return cursor_result

    @with_session
    async def query_one(
            self,
            cols: list = None,
            orm_table: Type[BaseOrmTable] = None,
            conds: list = None,
            orders: list = None,
            flat: bool = False,
            session: AsyncSession = None,
    ) -> Union[dict, T_BaseOrmTable, Any]:
        """
        查询单行
        Args:
            cols: 查询的列表字段
            orm_table: orm表映射类
            conds: 查询的条件列表
            orders: 排序列表
            flat: 单字段时扁平化处理
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Notes:
            # 指定列名
            ret = await UserManager().query_one(cols=["username", "age"], conds=[UserTable.id == 1])
            sql => select username, age from user where id=1
            ret => {"username": "hui", "age": 18}

            # 指定列名，单字段扁平化处理
            ret = await UserManager().query_one(cols=["username"], conds=[UserTable.id == 1])
            sql => select username from user where id=1
            ret => {"username": "hui"} => "hui"

            # 计算总数
            ret = await UserManager().query_one(cols=[func.count()])
            sql => select count(*) as count from user
            ret => {"count": 10} => 10

            # 不指定列名，查询全部字段, 返回表实例对象
            ret = await UserManager().query_one(conds=[UserTable.id == 1])
            sql => select id, username, age from user where id=1
            ret => UserTable(id=1, username="hui", age=18)

        Returns:
            Union[dict, BaseOrmTable(), Any(flat=True)]
        """
        cursor_result = await self._query(cols=cols, orm_table=orm_table, conds=conds, orders=orders, session=session)
        if cols:
            if flat and len(cols) == 1:
                # 单行单字段查询: 直接返回字段结果
                # eg: select count(*) as count from user 从 {"count": 100} => 100
                # eg: select username from user where id=1 从 {"username": "hui"} => "hui"
                return cursor_result.scalar_one()

            # eg: select username, age from user where id=1 => {"username": "hui", "age": 18}
            return cursor_result.mappings().one() or {}
        else:
            # 未指定列名查询默认全部字段，返回的是表实例对象 BaseOrmTable()
            # eg: select id, username, age from user where id=1 => UserTable(id=1, username="hui", age=18)
            return cursor_result.scalar_one()

    @with_session
    async def query_all(
            self,
            cols: list = None,
            orm_table: BaseOrmTable = None,
            conds: list = None,
            orders: list = None,
            flat: bool = False,
            limit: int = None,
            offset: int = None,
            session: AsyncSession = None,
    ) -> Union[List[dict], List[T_BaseOrmTable], Any]:
        """
        查询多行
        Args:
            cols: 查询的列表字段
            orm_table: orm表映射类
            conds: 查询的条件列表
            orders: 排序列表
            flat: 单字段时扁平化处理
            limit: 限制数量大小
            offset: 偏移量
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务
        """
        cursor_result = await self._query(
            cols=cols, orm_table=orm_table, conds=conds, orders=orders, limit=limit, offset=offset, session=session
        )
        if cols:
            if flat and len(cols) == 1:
                # 扁平化处理
                # eg: select id from user 从 [{"id": 1}, {"id": 2}, {"id": 3}] => [1, 2, 3]
                return cursor_result.scalars().all()

            # eg: select username, age from user => [{"username": "hui", "age": 18}, [{"username": "dbk", "age": 18}]]
            return cursor_result.mappings().all() or []
        else:
            # 未指定列名查询默认全部字段，返回的是表实例对象 [BaseOrmTable()]
            # eg: select id, username, age from user
            # [User(id=1, username="hui", age=18), User(id=2, username="dbk", age=18)
            return cursor_result.scalars().all()

    @with_session
    async def list_page(
            self,
            cols: list = None,
            orm_table: BaseOrmTable = None,
            conds: list = None,
            orders: list = None,
            curr_page: int = 1,
            page_size: int = 20,
            session: AsyncSession = None,
    ):
        """
        单表通用分页查询
        Args:
            cols: 查询的列表字段
            orm_table: orm表映射类
            conds: 查询的条件列表
            orders: 排序列表
            curr_page: 页码
            page_size: 每页数量
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns: total_count, data_list
        """
        conds = conds or []
        orders = orders or [column("id")]
        orm_table = orm_table or self.orm_table

        limit = page_size
        offset = (curr_page - 1) * page_size
        total_count, data_list = await asyncio.gather(
            self.query_one(
                cols=[func.count()], orm_table=orm_table, conds=conds, orders=orders, flat=True, session=session
            ),
            self.query_all(
                cols=cols, orm_table=orm_table, conds=conds, orders=orders, limit=limit, offset=offset, session=session
            ),
        )

        return total_count, data_list

    @with_session
    async def update(
            self,
            values: dict,
            orm_table: Type[BaseOrmTable] = None,
            conds: list = None,
            session: AsyncSession = None,
    ):
        """
        更新数据
        Args:
            values: 要更新的字段和对应的值，字典格式，例如 {"field1": value1, "field2": value2, ...}
            orm_table: ORM表映射类
            conds: 更新条件列表，每个条件为一个表达式，例如 [UserTable.username == "hui", ...]
            session: 数据库会话对象，如果为 None，则在方法内部开启新的事务

        Returns: 影响的行数
            cursor_result.rowcount
        """
        orm_table = orm_table or self.orm_table
        conds = conds or []
        values = values or {}
        if not values:
            return
        sql = update(orm_table).where(*conds).values(**values)
        cursor_result = await session.execute(sql)
        return cursor_result.rowcount

    @with_session
    async def run_sql(
            self,
            sql: str,
            params: dict = None,
            query_one: bool = False,
            session: AsyncSession = None
    ) -> Union[dict, List[dict]]:
        """
        执行并提交单条sql
        Args:
            sql: sql语句
            params: sql参数, eg. {":id_val": 10, ":name_val": "hui"}
            query_one: 是否查询单条，默认False查询多条
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns:
            执行sql的结果
        """
        sql = text(sql)
        cursor_result = await session.execute(sql, params)
        if query_one:
            return cursor_result.mappings().one() or {}
        else:
            return cursor_result.mappings().all() or []
