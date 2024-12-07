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
from typing import Any, AsyncIterator, List, Type, TypeVar, Union

from loguru import logger
from sqlalchemy import Result, column, delete, func, select, text, update
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from py_tools.connections.db.mysql import BaseOrmTable
from py_tools.meta_cls import SingletonMetaCls

T_BaseOrmTable = TypeVar("T_BaseOrmTable", bound=BaseOrmTable)
T_Hints = TypeVar("T_Hints")  # 用于修复被装饰的函数参数提示，让IDE有类型提示


def with_session(method) -> T_Hints:
    """
    兼容事务
    Args:
        method: orm 的 crud

    Notes:
        方法中没有带事务连接, 优先从方法参数中获取, 其次实例对象中获取，都没有则构造

    Returns:
    """

    @functools.wraps(method)
    async def wrapper(db_manager, *args, **kwargs):
        session = kwargs.get("session") or db_manager.session or None
        if session:
            kwargs["session"] = session
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
        session_options: dict = None,
        log: Union[logging.Logger] = None,
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
        self.session_options = session_options or {}

    def get_db_url(self, protocol: str = "mysql+aiomysql"):
        db_url = self.DB_URL_TEMPLATE.format(
            protocol=protocol, user=self.user, password=self.password, host=self.host, port=self.port, db=self.db_name
        )
        return db_url

    def init_db_engine(self, protocol: str, echo: bool = False, **kwargs) -> AsyncEngine:
        """
        初始化db引擎
        Args:
            protocol: 驱动协议类型
            echo: 控制是否打印sql执行详情

        Returns:
            self.db_engine
        """
        db_url = self.get_db_url(protocol=protocol)
        self.log.debug(f"init_db_engine => {db_url}")
        self.db_engine = create_async_engine(
            url=db_url,
            pool_size=self.pool_size,
            pool_pre_ping=self.pool_pre_ping,
            pool_recycle=self.pool_recycle,
            echo=echo,
            **kwargs,
        )
        if not self.session_options.get("expire_on_commit"):
            self.session_options["expire_on_commit"] = False
        self.async_session_maker = async_sessionmaker(bind=self.db_engine, **self.session_options)
        return self.db_engine

    def init_mysql_engine(self, protocol: str = "mysql+aiomysql", echo: bool = False, **kwargs):
        """
        初始化mysql引擎
        Args:
            protocol: 驱动协议类型
            echo: 控制是否打印sql执行详情

        Returns:
            self.db_engine
        """
        return self.init_db_engine(protocol=protocol, echo=echo, **kwargs)


class DBManager(metaclass=SingletonMetaCls):
    DB_CLIENT: SQLAlchemyManager = None
    orm_table: Type[BaseOrmTable] = None

    def __init__(self, session: AsyncSession = None):
        self.session = session

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

    @classmethod
    @asynccontextmanager
    async def connection(cls) -> AsyncIterator[AsyncConnection]:
        """数据库引擎连接上下文管理器"""
        async with cls.DB_CLIENT.db_engine.begin() as conn:
            yield conn

    @with_session
    async def bulk_delete_by_ids(
        self,
        pk_ids: list,
        *,
        orm_table: Type[BaseOrmTable] = None,
        logic_del: bool = False,
        logic_field: str = "deleted_at",
        logic_del_set_value: Any = None,
        session: AsyncSession = None,
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
        session = session or self.session
        orm_table = orm_table or self.orm_table
        conds = [orm_table.id.in_(pk_ids)]
        return await self.delete(
            conds=conds,
            orm_table=orm_table,
            logic_del=logic_del,
            logic_field=logic_field,
            logic_del_set_value=logic_del_set_value,
            session=session,
        )

    @with_session
    async def delete_by_id(
        self,
        pk_id: int,
        *,
        orm_table: Type[BaseOrmTable] = None,
        logic_del: bool = False,
        logic_field: str = "deleted_at",
        logic_del_set_value: Any = None,
        session: AsyncSession = None,
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
        session = session or self.session
        orm_table = orm_table or self.orm_table
        conds = [orm_table.id == pk_id]
        return await self.delete(
            conds=conds,
            orm_table=orm_table,
            logic_del=logic_del,
            logic_field=logic_field,
            logic_del_set_value=logic_del_set_value,
            session=session,
        )

    @with_session
    async def delete(
        self,
        *,
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
            conds: 条件列表, e.g. [UserTable.id == 1]
            orm_table: orm表映射类
            logic_del: 逻辑删除，默认 False 物理删除 True 逻辑删除
            logic_field: 逻辑删除字段 默认 deleted_at
            logic_del_set_value: 逻辑删除字段设置的值
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns: 删除的记录数
        """
        session = session or self.session
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
    async def bulk_add(
        self,
        table_objs: List[Union[T_BaseOrmTable, dict]],
        *,
        orm_table: Type[BaseOrmTable] = None,
        flush: bool = False,
        session: AsyncSession = None,
    ) -> List[T_BaseOrmTable]:
        """
        批量插入
        Args:
            table_objs: orm映射类实例列表
                e.g. [UserTable(username="hui", age=18), ...] or [{"username": "hui", "age": 18}, ...]
            orm_table: orm表映射类
            flush: 刷新对象状态，默认不刷新
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns:
            成功插入的对象列表
        """
        session = session or self.session
        orm_table = orm_table or self.orm_table
        if all(isinstance(table_obj, dict) for table_obj in table_objs):
            # 字典列表转成orm映射类实例列表处理
            table_objs = [orm_table(**table_obj) for table_obj in table_objs]

        session.add_all(table_objs)
        if flush:
            await session.flush(table_objs)

        return table_objs

    @with_session
    async def add(
        self, table_obj: [T_BaseOrmTable, dict], *, orm_table: Type[BaseOrmTable] = None, session: AsyncSession = None
    ) -> int:
        """
        插入一条数据
        Args:
            table_obj: orm映射类实例对象, eg. UserTable(username="hui", age=18) or {"username": "hui", "age": 18}
            orm_table: orm表映射类
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns: 新增的id
            table_obj.id
        """
        session = session or self.session
        orm_table = orm_table or self.orm_table
        if isinstance(table_obj, dict):
            table_obj = orm_table(**table_obj)

        session.add(table_obj)
        await session.flush(objects=[table_obj])  # 刷新对象状态，获取新增的id
        return table_obj.id

    @with_session
    async def query_by_id(
        self,
        pk_id: int,
        *,
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
        session = session or self.session
        orm_table = orm_table or self.orm_table
        ret = await session.get(orm_table, pk_id)
        return ret

    @with_session
    async def _query(
        self,
        *,
        cols: list = None,
        orm_table: BaseOrmTable = None,
        join_tables: list = None,
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
            join_tables: 连表信息 [(table, conds, join_type), ...]
                eg: [(UserProjectMappingTable, ProjectTable.id == UserProjectMappingTable.project_id, "left")]
            conds: 查询的条件列表
            orders: 排序列表, 默认id升序
            limit: 限制数量大小
            offset: 偏移量
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns: 查询结果集
            cursor_result
        """
        session = session or self.session
        cols = cols or []
        cols = [column(col_obj) if isinstance(col_obj, str) else col_obj for col_obj in cols]  # 兼容字符串列表

        join_tables = join_tables or []
        conditions = conds or []
        orders = orders or []
        orm_table = orm_table or self.orm_table

        # 构造查询
        if not cols:
            if join_tables:
                # 没有指定查询列，查询连表的所有列
                all_tables = [orm_table] + [join_table[0] for join_table in join_tables]
                cols = [col for table in all_tables for col in table.__table__.columns]
                query_sql = select(*cols).select_from(orm_table)
            else:
                # 没有指定查询列，没有连表，查询所有列（返回orm 实例）
                query_sql = select(orm_table)

        else:
            query_sql = select(*cols).select_from(orm_table)

        # 构造连表
        if join_tables:
            query_sql = await self._build_join(join_tables, query_sql)

        query_sql = query_sql.where(*conditions).order_by(*orders)
        if limit:
            query_sql = query_sql.limit(limit).offset(offset)

        # 执行查询
        cursor_result = await session.execute(query_sql)
        return cursor_result

    async def _build_join(self, join_tables: list, query_sql):
        """
        构造连表
        Args:
            join_tables: 连表信息 [(table, conds, join_type)]
                eg: [(UserProjectMappingTable, ProjectTable.id == UserProjectMappingTable.project_id, "left")]
            query_sql: 查询sql

        Returns:
            query_sql
        """
        for join_entry in join_tables:
            join_entry_num = len(join_entry)
            if join_entry_num < 2:
                raise ValueError("join_tables must have at least 2 columns")

            if join_entry_num == 2:
                join_table, join_condition = join_entry
                join_type = None  # Default to inner join
            else:
                join_table, join_condition, join_type, *_ = join_entry

            # Determine join type
            isouter = join_type == "left"
            query_sql = query_sql.join(join_table, join_condition, isouter=isouter)
        return query_sql

    @with_session
    async def query_one(
        self,
        *,
        cols: list = None,
        orm_table: Type[BaseOrmTable] = None,
        join_tables: list = None,
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
            join_tables: 连表信息(table, conds, join_type)
                eg: (UserProjectMappingTable, ProjectTable.id == UserProjectMappingTable.project_id, "left")
            conds: 查询的条件列表
            orders: 排序列表
            flat: 单字段时扁平化处理
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Examples:
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
        session = session or self.session
        cursor_result = await self._query(
            cols=cols, orm_table=orm_table, join_tables=join_tables, conds=conds, orders=orders, session=session
        )

        # fix circular import
        from py_tools.utils import SerializerUtil

        if cols:
            if flat and len(cols) == 1:
                # 单行单字段查询: 直接返回字段结果
                # eg: select count(*) as count from user 从 {"count": 100} => 100
                # eg: select username from user where id=1 从 {"username": "hui"} => "hui"
                return cursor_result.scalar_one_or_none()

            # eg: select username, age from user where id=1 => {"username": "hui", "age": 18}
            ret = cursor_result.mappings().one_or_none() or {}
            return SerializerUtil.model_to_data(ret)
        else:
            # 未指定列名查询默认全部字段，返回的是表实例对象 BaseOrmTable()
            # eg: select id, username, age from user where id=1 => UserTable(id=1, username="hui", age=18)
            if join_tables:
                # 连表还是返回 dict
                ret = cursor_result.mappings().one_or_none() or {}
                return SerializerUtil.model_to_data(ret)
            return cursor_result.scalar_one_or_none() or {}

    @with_session
    async def query_all(
        self,
        *,
        cols: list = None,
        orm_table: BaseOrmTable = None,
        join_tables: list = None,
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
            join_tables: 连表信息[(table, conds, join_type)]
                eg: [(UserProjectMappingTable, ProjectTable.id == UserProjectMappingTable.project_id, "left")]
            conds: 查询的条件列表
            orders: 排序列表
            flat: 单字段时扁平化处理
            limit: 限制数量大小
            offset: 偏移量
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务
        """
        # session = session or self.session
        cursor_result = await self._query(
            cols=cols,
            orm_table=orm_table,
            join_tables=join_tables,
            conds=conds,
            orders=orders,
            limit=limit,
            offset=offset,
            session=session,
        )

        # fix circular import
        from py_tools.utils import SerializerUtil

        if cols:
            if flat and len(cols) == 1:
                # 扁平化处理
                # eg: select id from user 从 [{"id": 1}, {"id": 2}, {"id": 3}] => [1, 2, 3]
                return cursor_result.scalars().all() or []

            # eg: select username, age from user => [{"username": "hui", "age": 18}, [{"username": "dbk", "age": 18}]]
            ret = cursor_result.mappings().all() or []
            return SerializerUtil.model_to_data(ret)
        else:
            # 未指定列名查询默认全部字段，
            if join_tables:
                # 连表查询还是返回 dict 列表
                ret = cursor_result.mappings().all() or []
                return SerializerUtil.model_to_data(ret)

            # 返回的是表实例对象 [BaseOrmTable()]
            # eg: select id, username, age from user
            # [User(id=1, username="hui", age=18), User(id=2, username="dbk", age=18)
            return cursor_result.scalars().all() or []

    async def list_page(
        self,
        cols: list = None,
        orm_table: BaseOrmTable = None,
        join_tables: list = None,
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
            join_tables: 连表信息[(table, conds, join_type)]
                eg: [(UserProjectMappingTable, ProjectTable.id == UserProjectMappingTable.project_id, "left")]
            conds: 查询的条件列表
            orders: 排序列表
            curr_page: 页码
            page_size: 每页数量
            session: 数据库会话对象，如果为 None，则通过装饰器在方法内部开启新的事务

        Returns: total_count, data_list
        """
        session = session or self.session
        conds = conds or []
        orders = orders or []
        orm_table = orm_table or self.orm_table

        limit = page_size
        offset = (curr_page - 1) * page_size
        total_count, data_list = await asyncio.gather(
            self.query_one(
                cols=[func.count()],
                orm_table=orm_table,
                join_tables=join_tables,
                conds=conds,
                orders=orders,
                flat=True,
                session=session,
            ),
            self.query_all(
                cols=cols,
                orm_table=orm_table,
                join_tables=join_tables,
                conds=conds,
                orders=orders,
                limit=limit,
                offset=offset,
                session=session,
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
        session = session or self.session
        orm_table = orm_table or self.orm_table
        conds = conds or []
        values = values or {}
        if not values:
            return
        sql = update(orm_table).where(*conds).values(**values)
        cursor_result = await session.execute(sql)
        return cursor_result.rowcount

    @with_session
    async def update_or_add(
        self,
        table_obj: [T_BaseOrmTable, dict],
        *,
        orm_table: Type[BaseOrmTable] = None,
        session: AsyncSession = None,
        **kwargs,
    ):
        """
        指定对象更新or添加数据
        Args:
            table_obj: 映射类实例对象 or dict，
                e.g. UserTable(username="hui", age=18) or {"username": "hui", "v": 18, ...}
            orm_table: ORM表映射类
            session: 数据库会话对象，如果为 None，则在方法内部开启新的事务

        Returns:
        """
        session = session or self.session
        orm_table = orm_table or self.orm_table
        if isinstance(table_obj, dict):
            table_obj = orm_table(**table_obj)

        return await session.merge(table_obj, **kwargs)

    @with_session
    async def run_sql(
        self, sql: str, *, params: dict = None, query_one: bool = False, session: AsyncSession = None
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
        session = session or self.session
        sql = text(sql)
        cursor_result = await session.execute(sql, params)
        if query_one:
            return cursor_result.mappings().one() or {}
        else:
            return cursor_result.mappings().all() or []
