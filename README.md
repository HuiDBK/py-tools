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
默认安装如下功能可以使用
- 时间工具类
- http客户端
- 同步异步互转装饰器
- 常用枚举
- pydantic
- loguru的日志器
- 等...

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
    "cache-proxy": ["redis>=4.5.4", "python-memcached==1.62", "cacheout==0.14.1"], # 缓存代理
    "minio": ["minio==7.1.17"],
    "excel-tools": ["pandas==1.3.5", "openpyxl==3.0.10"], # excel工具类
}
```

### 简单使用
> 所有功能都是从 py_tools 包中导入使用
> 详细使用请查看项目的DEMO： https://github.com/HuiDBK/py-tools/tree/master/demo

生成python项目结构模板
```python
py_tools make_project WebDemo
```

mysql数据库操作demo
```python
import asyncio
import uuid
from typing import List

from connections.sqlalchemy_demo.manager import UserFileManager
from connections.sqlalchemy_demo.table import UserFileTable
from sqlalchemy import func

from py_tools.connections.db.mysql import BaseOrmTable, DBManager, SQLAlchemyManager

db_client = SQLAlchemyManager(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="123456",
    db_name="hui-demo",
)


async def create_and_transaction_demo():
    async with UserFileManager.transaction() as session:
        await UserFileManager().bulk_add(table_objs=[{"filename": "aaa", "oss_key": uuid.uuid4().hex}], session=session)
        user_file_obj = UserFileTable(filename="eee", oss_key=uuid.uuid4().hex)
        file_id = await UserFileManager().add(table_obj=user_file_obj, session=session)
        print("file_id", file_id)

        ret: UserFileTable = await UserFileManager().query_by_id(2, session=session)
        print("query_by_id", ret)

        # a = 1 / 0

        ret = await UserFileManager().query_one(
            cols=[UserFileTable.filename, UserFileTable.oss_key], conds=[UserFileTable.filename == "ccc"], session=session
        )
        print("ret", ret)


async def query_demo():
    ret = await UserFileManager().query_one(conds=[UserFileTable.filename == "ccc"])
    print("ret", ret)

    file_count = await UserFileManager().query_one(cols=[func.count()], flat=True)
    print("str col one ret", file_count)

    filename = await UserFileManager().query_one(cols=[UserFileTable.filename], conds=[UserFileTable.id == 2], flat=True)
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
    data_ret = await UserFileManager().run_sql(data_sql, params=params)
    print("dict data_ret", data_ret)

    # 连表查询
    data_sql = """
    select
        user.id as user_id,
        username,
        user_file.id as file_id,
        filename,
        oss_key
    from 
        user_file
        join user on user.id = user_file.creator
    where 
        user_file.creator = :user_id
    """
    data_ret = await UserFileManager().run_sql(data_sql, params={"user_id": 1})
    print("join sql data_ret", data_ret)


async def curd_demo():
    await create_and_transaction_demo()
    await query_demo()
    await list_page_demo()
    await run_raw_sql_demo()


async def create_tables():
    # 根据映射创建库表
    async with DBManager.connection() as conn:
        await conn.run_sync(BaseOrmTable.metadata.create_all)


async def main():
    db_client.init_mysql_engine()
    DBManager.init_db_client(db_client)
    await create_tables()
    await curd_demo()


if __name__ == "__main__":
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
1. [x] 超时装饰器
2. [x] 重试装饰器
3. [x] 缓存装饰器
4. [x] 异步执行装饰器

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
