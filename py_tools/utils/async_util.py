#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: async.py
# @Desc: { 异步工具模块 }
# @Date: 2024/04/24 15:20
import asyncio
import functools
from concurrent.futures import Executor, ThreadPoolExecutor
from typing import Any, Coroutine, List

from asgiref.sync import async_to_sync, sync_to_async


class AsyncUtil:
    # 线程池
    BASE_EXECUTOR = ThreadPoolExecutor()

    # 默认并发限制
    DEFAULT_NUM_WORKERS = 5

    # 同步异步互转
    AsyncToSync = async_to_sync
    SyncToAsync = sync_to_async

    @staticmethod
    def get_asyncio_module(show_progress: bool = False) -> Any:
        if show_progress:
            from tqdm.asyncio import tqdm_asyncio

            module = tqdm_asyncio
        else:
            module = asyncio

        return module

    @classmethod
    def run_bg_task(cls, func, *args, executor: Executor = None, **kwargs):
        """运行后台任务"""
        if asyncio.iscoroutine(func):
            # 协程对象处理
            return asyncio.create_task(func)

        executor = executor or cls.BASE_EXECUTOR

        return executor.submit(func, *args, **kwargs)

    @classmethod
    async def async_run(cls, func, *args, executor: Executor = None, **kwargs):
        """同步方法使用线程池异步运行"""
        loop = asyncio.get_event_loop()
        task_func = functools.partial(func, *args, **kwargs)  # 支持关键字参数
        executor = executor or cls.BASE_EXECUTOR
        return await loop.run_in_executor(executor, task_func)

    @staticmethod
    def sync_run(coro_obj: Coroutine):
        """同步环境运行异步方法"""
        return asyncio.run(coro_obj)

    @classmethod
    async def run_jobs(
        cls,
        jobs: List[Coroutine],
        show_progress: bool = False,
        workers: int = DEFAULT_NUM_WORKERS,
    ) -> List[Any]:
        """Run jobs.

        Args:
            jobs (List[Coroutine]):
                List of jobs to run.
            show_progress (bool):
                Whether to show progress bar.
            workers: 默认并发数

        Returns:
            List[Any]:
                List of results.
        """
        asyncio_mod = cls.get_asyncio_module(show_progress=show_progress)
        semaphore = asyncio.Semaphore(workers)

        async def worker(job: Coroutine) -> Any:
            async with semaphore:
                return await job

        pool_jobs = [worker(job) for job in jobs]

        return await asyncio_mod.gather(*pool_jobs)


class NestAsyncio:
    """Make asyncio event loop reentrant."""

    is_applied = False

    @classmethod
    def apply_once(cls):
        """Ensures `nest_asyncio.apply()` is called only once."""
        if not cls.is_applied:
            import nest_asyncio

            nest_asyncio.apply()
            cls.is_applied = True
