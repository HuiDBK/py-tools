# Py-Tools

> Py-Tools 是一个实用的 Python 工具集和可复用组件库，旨在简化常见任务，提高 Python 项目的开发效率。
> 
> 设计细节请移步到掘金查看：https://juejin.cn/column/7131286129713610766

## 安装
- 环境要求：python version >= 3.7
- 历史版本记录：https://pypi.org/project/hui-tools/#history


### 默认安装
```python
pip install hui-tools
```
默认安装只会安装loguru的日志库和pydantic，使用的功能较少


### 全部安装
```python
pip install hui-tools[all]
```

### 可选安装
```python
pip install hui-tools[db-orm, db-redis, excel-tools]
```

可选参数参考：
```python
extras_require = {
    "db-orm": ["sqlalchemy[asyncio]==2.0.20", "aiomysql==0.2.0"], # 数据库orm
    "db-redis": ["redis>=4.5.4"], # redis
    "minio": ["minio==7.1.17"],
    "chatbot": ["requests==2.31.0", "cacheout==0.14.1"], # 飞书、钉钉、企业微信机器人通知
    "http-client": ["httpx==0.24.1", "requests==2.31.0"], # http 同步、异步客户端
    "time-tools": ["python-dateutil==2.8.2"], # 时间工具类
    "excel-tools": ["pandas==1.3.5", "openpyxl==3.0.10"], # excel工具类
}
```

### 简单使用
> 所有功能都是从 py_tools 包中导入使用
> 详细使用请查看项目的DEMO： https://github.com/HuiDBK/py-tools/tree/master/demo


sqlalchemy 通用DBManager封装细节与使用Demo
部分封装展示
```python
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
```


部分使用demo，详情请到 demo/connections/sqlalchemy_demo/demo.py 文件查阅
```python
async def create_and_transaction_demo():
    async with UserFileManager.transaction() as session:
        await UserFileManager().bulk_insert(
            add_rows=[{"filename": "aaa", "oss_key": uuid.uuid4().hex}], session=session
        )
        user_file_obj = UserFileTable(filename="eee", oss_key=uuid.uuid4().hex)
        file_id = await UserFileManager().add(table_obj=user_file_obj, session=session)
        print("file_id", file_id)

        ret: UserFileTable = await UserFileManager().query_by_id(2, session=session)
        print("query_by_id", ret)

        # a = 1 / 0

        ret = await UserFileManager().query_one(
            cols=[UserFileTable.filename, UserFileTable.oss_key],
            conds=[UserFileTable.filename == "ccc"],
            session=session
        )
        print("ret", ret)


async def query_demo():
    ret = await UserFileManager().query_one(conds=[UserFileTable.filename == "ccc"])
    print("ret", ret)

    file_count = await UserFileManager().query_one(cols=[func.count()], flat=True)
    print("str col one ret", file_count)

    filename = await UserFileManager().query_one(
        cols=[UserFileTable.filename],
        conds=[UserFileTable.id == 2],
        flat=True
    )
    print("filename", filename)

    ret = await UserFileManager().query_all(cols=[UserFileTable.filename, UserFileTable.oss_key])
    print("ret", ret)

    ret = await UserFileManager().query_all(cols=["filename", "oss_key"])
    print("str col ret", ret)

    ret: List[UserFileTable] = await UserFileManager().query_all()
    print("ret", ret)

    ret = await UserFileManager().query_all(cols=[UserFileTable.id], flat=True)
    print("ret", ret)


async def list_page_demo():
    """分页查询demo"""
    total_count, data_list = await UserFileManager().list_page(
        cols=["filename", "oss_key", "file_size"], curr_page=2, page_size=10
    )
    print("total_count", total_count, f"data_list[{len(data_list)}]", data_list)


async def run_raw_sql_demo():
    """运行原生sql demo"""
    count_sql = "select count(*) as total_count from user_file"
    count_ret = await UserFileManager().run_sql(count_sql, query_one=True)
    print("count_ret", count_ret)

    data_sql = "select * from user_file where id > :id_val and file_size >= :file_size_val"
    params = {"id_val": 20, "file_size_val": 0}
    data_ret = await UserFileManager().run_sql(data_sql, params)
    print("dict data_ret", data_ret)

    data_sql = "select * from user_file where id > :id_val"
    data_ret = await UserFileManager().run_sql(sql=data_sql, params={"id_val": 4})
    print("dict data_ret", data_ret)

```


http 客户端举例
```python
import asyncio

from py_tools.enums import RespFmt
from py_tools.logging import logger
from py_tools.connections.http import HttpClient, AsyncHttpClient


async def async_http_client_demo():
    logger.debug("async_http_client_demo")
    url = "https://github.com/HuiDBK"

    # 调用
    data = await AsyncHttpClient().get(url, resp_fmt=RespFmt.TEXT)
    logger.debug(data)


def sync_http_client_demo():
    logger.debug("sync_http_client_demo")
    url = "https://github.com/HuiDBK"
    text_content = HttpClient().get(url).text
    logger.debug(text_content)


async def main():
    await async_http_client_demo()

    sync_http_client_demo()


if __name__ == '__main__':
    asyncio.run(main())

```


## Todo List

### 连接客户端
1. [x] http 同步异步客户端
2. [x] MySQL客户端 - SQLAlchemy-ORM 封装 
3. [x] Minio 客户端 
4. 消息队列客户端，rabbitmq、kafka 
5. websocket 客户端

### 工具类
- 图片操作工具类，例如校验图片分辨率
- 配置解析工具类
- 编码工具类，统一 base64、md5等编码入口
- 认证相关工具类，例如jwt、oauth2等
- 邮件服务工具类
- 常用正则工具类

### 装饰器

### 枚举

### 异常

### 日志

## 工程目录结构

```
py-tools/
    ├── py_tools/
    │   ├── chatbot/
    │   ├── connections/
    │   ├── constants/
    │   ├── data_models/
    │   ├── decorators/
    │   ├── enums/
    │   ├── exceptions/
    │   ├── meta_cls/
    │   └── utils/
    ├── docs/
    ├── demo/
    ├── tests/
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    └── requirements.txt
```



### 项目模块

- **chatbot**: 用于构建和管理聊天机器人互动的工具集。
- **connections**: 用于连接各种服务和 API 的连接管理工具。
- **constants**: Python 项目中常用的常量。
- **data_models**: 用于处理结构化数据的数据模型及相关工具。
- **decorators**: 一系列有用的装饰器，用以增强函数和方法。
- **enums**: 定义常用枚举类型，方便在项目中使用。
- **exceptions**: 自定义异常类，用于项目中的错误处理。
- **meta_cls**: 元类和元编程相关的工具和技术。
- **utils**: 包含各种实用函数和工具，用于简化日常编程任务。



### 项目文档

在 `docs` 目录下存放一些项目相关文档。



### 示例

在 `demo` 目录下，您可以找到一些使用 Py-Tools 的示例代码，这些代码展示了如何使用这些工具集实现实际项目中的任务。

demo：https://github.com/HuiDBK/py-tools/tree/master/demo

### 测试

在 `tests` 目录下，包含了针对 Py-Tools 的各个组件的单元测试。通过运行这些测试，您可以确保工具集在您的环境中正常工作。



## 一起贡献
> 欢迎您对本项目进行贡献。请在提交 Pull Request 之前阅读项目的贡献指南，并确保您的代码符合项目的代码风格。

1. 克隆本项目到本地：
```bash
git clone https://github.com/HuiDBK/py-tools.git
```

2. 安装依赖:
```python
pip install -r requirements.txt
```

3. 配置python代码风格检查到 git hook 中

安装 pre-commit
```python
pip install pre-commit
```

再项目目录下执行
```python
pre-commit install
```
安装成功后 git commit 后会提前进行代码检查

4. 提PR
