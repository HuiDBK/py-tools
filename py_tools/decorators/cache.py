#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 缓存装饰器模块 }
# @Date: 2023/05/03 19:23
import asyncio
import functools
import hashlib
import json
from dataclasses import dataclass
from typing import Type
from py_tools import constants


@dataclass
class CacheMeta:
    """缓存元信息"""

    key: str  # 缓存的key
    ttl: int  # 缓存有效期
    type: str = None  # 缓存的类型（Redis）
    data_type: str = None  # 缓存的数据类型（str、list、hash、set）


class BaseCacheProxy(object):
    """缓存代理抽象类"""

    def __init__(self, cache_client):
        self.cache_client = cache_client  # 具体的缓存客户端，例如Redis、Memcached等

    def set(self, key, value, ttl):
        raise NotImplemented

    def get(self, key):
        raise NotImplemented


class RedisCacheProxy(BaseCacheProxy):
    """redis缓存代理"""

    def set(self, key, value, ttl):
        value = json.dumps(value)
        self.cache_client.set(key, value, ttl)

    def get(self, key):
        cache_data = self.cache_client.get(key)
        cache_data = json.loads(cache_data)
        return cache_data


class AsyncRedisCacheProxy(BaseCacheProxy):
    """异步缓存代理"""

    async def set(self, key, value, ttl):
        value = json.dumps(value)
        await self.cache_client.set(key, value, ttl)

    async def get(self, key):
        cache_data = await self.cache_client.get(key)
        cache_data = json.loads(cache_data)
        return cache_data


def cache_json(
        cache_proxy: Type[BaseCacheProxy],
        key: str = None,
        ttl: int = 60,
        cache_meta: CacheMeta = None,
        def_key_prefix: str = constants.CACHE_KEY_PREFIX,
):
    """
    缓存装饰器（仅支持缓存能够json序列化的数据）
    Args:
        cache_proxy: 缓存代理对象
        key: 缓存的key
        ttl: 过期时间 默认60s
        cache_meta: 缓存元信息
        def_key_prefix: 默认的key前缀, 再未指定key时使用

    Returns:
    """
    if cache_meta:
        # 有元信息直接覆盖key, ttl
        key = cache_meta.key
        ttl = cache_meta.ttl

    def _cache(func):

        def _gen_key(*args, **kwargs):
            """生成缓存的key"""

            nonlocal key
            if not key:
                # 没有传递key信息，根据函数信息与参数生成
                # key => 函数所在模块:函数名:函数位置参数:函数关键字参数 进行hash
                param_args_str = ",".join([str(arg) for arg in args])
                param_kwargs_str = ",".join(sorted([f"{k}:{v}" for k, v in kwargs.items()]))
                hash_str = f"{func.__module__}:{func.__name__}:{param_args_str}:{param_kwargs_str}"
                has_result = hashlib.md5(hash_str.encode()).hexdigest()

                # 根据哈希结果生成key 默认前缀:函数所在模块:函数名:hash
                key = f"{def_key_prefix}:{func.__module__}:{func.__name__}:{has_result}"

            return key

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            """同步处理"""

            # 生成缓存的key
            _key = _gen_key(*args, **kwargs)

            # 先从缓存获取数据
            cache_data = cache_proxy.get(_key)
            if cache_data:
                # 有直接返回
                return cache_data

            # 没有，执行函数获取结果
            ret = func(*args, **kwargs)

            # 缓存结果
            cache_proxy.set(key=_key, value=ret, ttl=ttl)
            return ret

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            """异步处理"""

            # 生成缓存的key
            _key = _gen_key(*args, **kwargs)

            # 先从缓存获取数据
            cache_data = await cache_proxy.get(_key)
            if cache_data:
                # 有直接返回
                return cache_data

            # 没有，执行函数获取结果
            ret = await func(*args, **kwargs)

            # 缓存结果
            await cache_proxy.set(key=_key, value=ret, ttl=ttl)
            return ret

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return _cache
