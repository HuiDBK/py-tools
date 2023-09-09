# Py-Tools

> Py-Tools 是一个实用的 Python 工具集和可复用组件库，旨在简化常见任务，提高 Python 项目的开发效率。
> 
> 设计细节请移步到掘金查看：https://juejin.cn/column/7131286129713610766

## 安装
- 环境要求：python version >= 3.7
- 历史版本记录：https://pypi.org/project/hui-tools/#history


### 默认安装
```python
pip install hui_tools
```
默认安装只会安装loguru的日志库和pydantic，使用的功能较少


### 全部安装
```python
pip install hui_tools[all]
```

### 可选安装
```python
pip install hui_tools[db-orm, db-redis, excel-tools]
```

可选参数参考：
```python
extras_require = {
   "db-orm": ["sqlalchemy[asyncio]==2.0.20", "aiomysql==0.2.0"], # 数据库orm
   "db-redis": ["redis==4.5.4", "aioredis==2.0.1"], # redis
   "chatbot": ["requests==2.31.0", "cacheout==0.14.1"], # 飞书、钉钉、企业微信机器人通知
   "http-client": ["httpx==0.24.1", "requests==2.31.0"], # http 同步、异步客户端
   "time-tools": ["python-dateutil==2.8.2"], # 时间工具类
   "excel-tools": ["pandas==1.3.5", "openpyxl==3.0.10"], # excel工具类
}
```

### 简单使用
> 所有功能都是从 py_tools 包中导入使用
> 详细使用请查看项目的DEMO： https://github.com/HuiDBK/py-tools/tree/master/demo

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
3. Minio 客户端 
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