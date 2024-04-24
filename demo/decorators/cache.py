#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: cache.py
# @Desc: { cache demo 模块 }
# @Date: 2024/04/23 11:11
import asyncio
import time
from datetime import timedelta

import cacheout

from py_tools.connections.db.redis_client import BaseRedisManager
from py_tools.decorators.cache import AsyncRedisCacheProxy, MemoryCacheProxy, RedisCacheProxy, cache_json


class RedisManager(BaseRedisManager):
    client = None


class AsyncRedisManager(BaseRedisManager):
    client = None


RedisManager.init_redis_client(async_client=False)
AsyncRedisManager.init_redis_client(async_client=True)

memory_proxy = MemoryCacheProxy(cache_client=cacheout.Cache())
redis_proxy = RedisCacheProxy(cache_client=RedisManager.client)
aredis_proxy = AsyncRedisCacheProxy(cache_client=AsyncRedisManager.client)


@cache_json(key_prefix="demo", ttl=3)
def memory_cache_demo_func(name: str, age: int):
    return {"test_memory_cache": "hui-test", "name": name, "age": age}


@cache_json(cache_proxy=redis_proxy, ttl=10)
def redis_cache_demo_func(name: str, age: int):
    return {"test_redis_cache": "hui-test", "name": name, "age": age}


@cache_json(cache_proxy=aredis_proxy, ttl=timedelta(minutes=1))
async def aredis_cache_demo_func(name: str, age: int):
    return {"test_async_redis_cache": "hui-test", "name": name, "age": age}


@AsyncRedisManager.cache_json(ttl=30)
async def aredis_manager_cache_demo_func(name: str, age: int):
    return {"test_async_redis_manager_cache": "hui-test", "name": name, "age": age}


def memory_cache_demo():
    print("memory_cache_demo")
    ret1 = memory_cache_demo_func(name="hui", age=18)
    print("ret1", ret1)
    print()

    ret2 = memory_cache_demo_func(name="hui", age=18)
    print("ret2", ret2)
    print()

    time.sleep(3)
    ret3 = memory_cache_demo_func(age=18, name="hui")
    print("ret3", ret3)
    print()

    assert ret1 == ret2 == ret3

    # ret4 = memory_cache_demo_func(name="huidbk", age=18)
    # print("ret4", ret4)
    # print()
    #
    # ret5 = memory_cache_demo_func(name="huidbk", age=20)
    # print("ret5", ret5)
    # print()
    #
    # assert ret4 != ret5
    #
    # ret6 = memory_cache_demo_func(name="huidbk", age=20)
    # print("ret6", ret6)
    # print()
    #
    # assert ret5 == ret6


def redis_cache_demo():
    print("redis_cache_demo")
    ret1 = redis_cache_demo_func(name="hui", age=18)
    print("ret1", ret1)
    print()

    ret2 = redis_cache_demo_func(name="hui", age=18)
    print("ret2", ret2)

    assert ret1 == ret2


async def aredis_cache_demo():
    print("aredis_cache_demo")
    ret1 = await aredis_cache_demo_func(name="hui", age=18)
    print("ret1", ret1)
    print()

    ret2 = await aredis_cache_demo_func(name="hui", age=18)
    print("ret2", ret2)

    assert ret1 == ret2


async def aredis_manager_cache_demo():
    print("aredis_manager_cache_demo")
    ret1 = await aredis_manager_cache_demo_func(name="hui", age=18)
    print("ret1", ret1)
    print()

    ret2 = await aredis_manager_cache_demo_func(name="hui", age=18)
    print("ret2", ret2)

    assert ret1 == ret2


async def main():
    memory_cache_demo()

    redis_cache_demo()

    await aredis_cache_demo()

    await aredis_manager_cache_demo()


if __name__ == "__main__":
    asyncio.run(main())
