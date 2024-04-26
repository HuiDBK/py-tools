#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: async.py
# @Desc: { 异步相关工具函数demo }
# @Date: 2024/04/24 15:32
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

from py_tools.utils.aio import run_bg_task, async_run, sync_run, async_to_sync, sync_to_async

BASE_EXECUTOR = ThreadPoolExecutor(max_workers=3)


async def async_bg_task(name, age):
    print(f"async_bg_task run... {name}, {age}")
    await asyncio.sleep(1)
    print("async_bg_task done")
    return name, age


def sync_bg_task(name, age):
    print(f"sync_bg_task run... {name}, {age}")
    time.sleep(1)
    print("sync_bg_task done")
    return name, age


async def main():
    run_bg_task(sync_bg_task, name="sync-hui", age=18)

    run_bg_task(async_bg_task(name="async-hui", age=18))
    # ret = await run_bg_task(async_bg_task(name="async-hui", age=18))
    # print(ret)

    future_task = run_bg_task(sync_bg_task, name="executor-sync-hui", age=18, executor=BASE_EXECUTOR)
    # print(future_task.result())

    await asyncio.sleep(5)

    ret = await async_run(sync_bg_task, name="async to sync", age=18, executor=BASE_EXECUTOR)
    print(ret)

    sync_to_async(sync_bg_task)(name="sync to async", age=18)


def async_to_sync_demo():
    ret = sync_run(async_bg_task(name="sync run async", age=18))
    print("sync_run", ret)

    ret = async_to_sync(async_bg_task)(name="async to async", age=18)
    print(ret)


if __name__ == '__main__':
    asyncio.run(main())
    async_to_sync_demo()
