#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: async.py
# @Desc: { 异步工具模块 }
# @Date: 2024/04/24 15:20
import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor, Executor

from asgiref.sync import async_to_sync, sync_to_async

# 线程池
BASE_EXECUTOR = ThreadPoolExecutor()


def run_bg_task(func, *args, executor: Executor = None, **kwargs):
    """运行后台任务"""
    if asyncio.iscoroutine(func):
        # 协程对象处理
        return asyncio.create_task(func)

    executor = executor or BASE_EXECUTOR

    return executor.submit(func, *args, **kwargs)


async def async_run(func, *args, executor: Executor = None, **kwargs):
    """同步方法使用线程池异步运行"""
    loop = asyncio.get_event_loop()
    task_func = functools.partial(func, *args, **kwargs)  # 支持关键字参数
    executor = executor or BASE_EXECUTOR
    return await loop.run_in_executor(executor, task_func)


def sync_run(coro_obj):
    """同步环境运行异步方法"""
    return asyncio.run(coro_obj)
