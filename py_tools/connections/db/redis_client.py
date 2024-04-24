#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { redis连接处理模块 }
# @Date: 2023/05/03 21:13
from datetime import timedelta
from typing import Optional, Union

from redis import Redis
from redis import asyncio as aioredis

from py_tools import constants
from py_tools.decorators.cache import AsyncRedisCacheProxy, CacheMeta, RedisCacheProxy, cache_json


class BaseRedisManager:
    """Redis客户端管理器"""

    client: Union[Redis, aioredis.Redis] = None
    cache_key_prefix = constants.CACHE_KEY_PREFIX

    @classmethod
    def init_redis_client(
        cls,
        async_client: bool = False,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
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
            password (Optional[str]): 密码可选
            max_connections (Optional[int]): 最大连接数。默认为 None（不限制连接数）
            **kwargs: 传递给 Redis 客户端的其他参数

        Returns:
            None
        """
        if cls.client is None:
            redis_client_cls = Redis
            if async_client:
                redis_client_cls = aioredis.Redis

            cls.client = redis_client_cls(
                host=host, port=port, db=db, password=password, max_connections=max_connections, **kwargs
            )

        return cls.client

    @classmethod
    def cache_json(
        cls,
        ttl: Union[int, timedelta] = 60,
        key_prefix: str = None,
    ):
        """
        缓存装饰器（仅支持缓存能够json序列化的数据）
        缓存函数整体结果
        Args:
            ttl: 过期时间 默认60s
            key_prefix: 默认的key前缀, 再未指定key时使用

        Returns:
        """
        key_prefix = key_prefix or cls.cache_key_prefix
        if isinstance(ttl, timedelta):
            ttl = int(ttl.total_seconds())

        cache_proxy = RedisCacheProxy(cls.client)
        if isinstance(cls.client, aioredis.Redis):
            cache_proxy = AsyncRedisCacheProxy(cls.client)

        return cache_json(cache_proxy=cache_proxy, key_prefix=key_prefix, ttl=ttl)
