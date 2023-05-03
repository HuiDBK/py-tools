#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { redis连接处理模块 }
# @Date: 2023/05/03 21:13
from typing import Optional, Union
import aioredis
from redis import Redis


class RedisManager:
    """Redis客户端管理器"""

    client: Union[Redis, aioredis.Redis] = None

    @classmethod
    def init_redis_client(
            cls,
            async_client: bool = False,
            host: str = 'localhost',
            port: int = 6379,
            db: int = 0,
            max_connections: Optional[int] = None,
            **kwargs
    ):
        """
        初始化 Redis 客户端。

        Args:
            async_client (bool): 是否使用异步客户端，默认为 False（同步客户端）
            host (str): Redis 服务器的主机名，默认为 'localhost'
            port (int): Redis 服务器的端口，默认为 6379
            db (int): 要连接的数据库编号，默认为 0
            max_connections (Optional[int]): 最大连接数。默认为 None（不限制连接数）
            **kwargs: 传递给 Redis 客户端的其他参数

        Returns:
            None
        """
        if cls.client is None:
            if async_client:
                cls.client = aioredis.Redis(host=host, port=port, db=db, max_connections=max_connections, **kwargs)
            else:
                cls.client = Redis(host=host, port=port, db=db, max_connections=max_connections, **kwargs)
