#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 缓存装饰器模块 }
# @Date: 2023/05/03 19:23
import asyncio
import functools
import hashlib
import json
from datetime import timedelta
from typing import Union

import cacheout
import memcache
from pydantic import BaseModel, Field
from redis import Redis
from redis import asyncio as aioredis

from py_tools import constants


class CacheMeta(BaseModel):
    """缓存元信息"""

    key: str = Field(description="缓存的key")
    ttl: Union[int, timedelta] = Field(description="缓存有效期")
    cache_client: str = Field(description="缓存的客户端（Redis、Memcached等）")
    data_type: str = Field(description="缓存的数据类型（str、list、hash、set）")


class BaseCacheProxy(object):
    """缓存代理基类"""

    def __init__(self, cache_client):
        self.cache_client = cache_client  # 具体的缓存客户端，例如Redis、Memcached等

    def set(self, key: str, value: str, ttl: int):
        raise NotImplementedError

    def get(self, key):
        cache_data = self.cache_client.get(key)
        return cache_data


class RedisCacheProxy(BaseCacheProxy):
    """同步redis缓存代理"""

    def __init__(self, cache_client: Redis):
        super().__init__(cache_client)

    def set(self, key, value, ttl):
        self.cache_client.setex(name=key, value=value, time=ttl)


class AsyncRedisCacheProxy(BaseCacheProxy):
    """异步Redis缓存代理"""

    def __init__(self, cache_client: aioredis.Redis):
        super().__init__(cache_client)

    async def set(self, key, value, ttl):
        await self.cache_client.setex(name=key, value=value, time=ttl)

    async def get(self, key):
        cache_data = await self.cache_client.get(key)
        return cache_data


class MemoryCacheProxy(BaseCacheProxy):
    """系统内存缓存代理"""

    def __init__(self, cache_client: cacheout.Cache):
        super().__init__(cache_client)

    def set(self, key, value, ttl):
        self.cache_client.set(key=key, value=value, ttl=ttl)


MEMORY_PROXY = MemoryCacheProxy(cache_client=cacheout.Cache(maxsize=1024))


class MemcacheCacheProxy(BaseCacheProxy):

    def __init__(self, cache_client: memcache.Client):
        super().__init__(cache_client)

    def set(self, key, value, ttl):
        self.cache_client.set(key, value, time=ttl)


def cache_json(
    cache_proxy: BaseCacheProxy = MEMORY_PROXY,
    key_prefix: str = constants.CACHE_KEY_PREFIX,
    ttl: Union[int, timedelta] = 60,
):
    """
    缓存装饰器（仅支持缓存能够json序列化的数据）
    Args:
        cache_proxy: 缓存代理客户端, 默认系统内存
        ttl: 过期时间 默认60s
        key_prefix: 默认的key前缀

    Returns:
    """
    key_prefix = f"{key_prefix}:cache_json"
    if isinstance(ttl, timedelta):
        ttl = int(ttl.total_seconds())

    def _cache(func):
        def _gen_key(*args, **kwargs):
            """生成缓存的key"""

            # 根据函数信息与参数生成
            # key => 函数所在模块:函数名:函数位置参数:函数关键字参数 进行hash
            param_args_str = ",".join([str(arg) for arg in args])
            param_kwargs_str = ",".join(sorted([f"{k}:{v}" for k, v in kwargs.items()]))
            hash_str = f"{func.__module__}:{func.__name__}:{param_args_str}:{param_kwargs_str}"
            hash_ret = hashlib.sha256(hash_str.encode()).hexdigest()

            # 根据哈希结果生成key 默认前缀:函数所在模块:函数名:hash
            hash_key = f"{key_prefix}:{func.__module__}:{func.__name__}:{hash_ret}"
            return hash_key

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            """同步处理"""

            # 生成缓存的key
            hash_key = _gen_key(*args, **kwargs)

            # 先从缓存获取数据
            cache_data = cache_proxy.get(hash_key)
            if cache_data:
                # 有直接返回
                print(f"命中缓存: {hash_key}")
                return json.loads(cache_data)

            # 没有，执行函数获取结果
            ret = func(*args, **kwargs)

            # 缓存结果
            cache_proxy.set(key=hash_key, value=json.dumps(ret), ttl=ttl)
            return ret

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            """异步处理"""

            # 生成缓存的key
            hash_key = _gen_key(*args, **kwargs)

            # 先从缓存获取数据
            cache_data = await cache_proxy.get(hash_key)
            if cache_data:
                # 有直接返回
                return json.loads(cache_data)

            # 没有，执行函数获取结果
            ret = await func(*args, **kwargs)

            # 缓存结果
            await cache_proxy.set(key=hash_key, value=json.dumps(ret), ttl=ttl)
            return ret

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return _cache
