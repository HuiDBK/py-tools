#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 通用装饰器模块 }
# @Date: 2022/11/26 16:16
import signal
import time
import asyncio
import threading
import functools
import traceback
from concurrent.futures import ThreadPoolExecutor, TimeoutError, Executor
from typing import Type, Callable

from loguru import logger

from py_tools.exceptions import MaxTimeoutException, MaxRetryException


def synchronized(func):
    """ 同步锁装饰器 """
    func.__lock__ = threading.Lock()

    @functools.wraps(func)
    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func


def singleton(cls_obj):
    """ 单例装饰器 """
    _instance_dic = {}
    _instance_lock = threading.Lock()

    @functools.wraps(cls_obj)
    def wrapper(*args, **kwargs):
        if cls_obj in _instance_dic:
            return _instance_dic.get(cls_obj)

        with _instance_lock:
            if cls_obj not in _instance_dic:
                _instance_dic[cls_obj] = cls_obj(*args, **kwargs)
        return _instance_dic.get(cls_obj)

    return wrapper


def calc_time(func):
    """ 执行时间计算装饰器 """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_ts = time.time()
        ret = func(*args, **kwargs)
        use_time = time.time() - start_ts
        logger.info(f"func {func.__name__} use {use_time}s")
        return ret

    return wrapper


def set_timeout(timeout: int, use_signal=False):
    """
    超时处理装饰器
    Args:
        timeout: 超时时间，单位秒
        use_signal: 使用信号量机制只能在 unix内核上使用，默认False

    Raises:
        TimeoutException

    """

    def _timeout(func: Callable):

        def _handle_timeout(signum, frame):
            raise MaxTimeoutException(f"Function timed out after {timeout} seconds")

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # 同步函数处理超时
            if use_signal:
                # 使用信号量计算超时
                signal.signal(signal.SIGALRM, _handle_timeout)
                signal.alarm(timeout)
                try:
                    return func(*args, **kwargs)
                finally:
                    signal.alarm(0)
            else:
                # 使用线程
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(func, *args, **kwargs)
                    try:
                        return future.result(timeout)
                    except TimeoutError:
                        raise MaxTimeoutException(f"Function timed out after {timeout} seconds")

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # 异步函数处理超时
            try:
                ret = await asyncio.wait_for(func(*args, **kwargs), timeout)
                return ret
            except asyncio.TimeoutError:
                raise MaxTimeoutException(f"Function timed out after {timeout} seconds")

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return _timeout


def retry(
        max_count: int = 5,
        interval: int = 2,
        catch_exc: Type[BaseException] = Exception
):
    """
    重试装饰器
    Args:
        max_count: 最大重试次数 默认 5 次
        interval: 每次异常重试间隔 默认 2s
        catch_exc: 指定捕获的异常类用于特定的异常重试 默认捕获 Exception

    Raises:
        MaxRetryException
    """

    def _retry(task_func):

        @functools.wraps(task_func)
        def sync_wrapper(*args, **kwargs):
            # 函数循环重试

            for retry_count in range(max_count):
                logger.info(f"{task_func} execute count {retry_count + 1}")
                try:
                    return task_func(*args, **kwargs)
                except catch_exc:
                    logger.error(f"fail {traceback.print_exc()}")
                    if retry_count < max_count - 1:
                        # 最后一次异常不等待
                        time.sleep(interval)

            # 超过最大重试次数, 抛异常终止
            raise MaxRetryException(f"超过最大重试次数失败, max_retry_count {max_count}")

        @functools.wraps(task_func)
        async def async_wrapper(*args, **kwargs):
            # 异步循环重试
            for retry_count in range(max_count):
                logger.info(f"{task_func} execute count {retry_count + 1}")

                try:
                    return await task_func(*args, **kwargs)
                except catch_exc as e:
                    logger.error(f"fail {str(e)}")
                    if retry_count < max_count - 1:
                        await asyncio.sleep(interval)

            # 超过最大重试次数, 抛异常终止
            raise MaxRetryException(f"超过最大重试次数失败, max_retry_count {max_count}")

        # 异步函数判断
        wrapper_func = async_wrapper if asyncio.iscoroutinefunction(task_func) else sync_wrapper
        return wrapper_func

    return _retry


def run_on_executor(executor: Executor = None, background: bool = False):
    """
    异步装饰器
    - 支持同步函数使用 executor 加速
    - 异步函数和同步函数都可以使用 `await` 语法等待返回结果
    - 异步函数和同步函数都支持后台任务，无需等待
    Args:
        executor: 函数执行器, 装饰同步函数的时候使用
        background: 是否后台执行，默认False

    Returns:
    """

    def _run_on_executor(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            if background:
                return asyncio.create_task(func(*args, **kwargs))
            else:
                return await func(*args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            loop = asyncio.get_event_loop()
            task_func = functools.partial(func, *args, **kwargs)    # 支持关键字参数
            return loop.run_in_executor(executor, task_func)

        # 异步函数判断
        wrapper_func = async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return wrapper_func

    return _run_on_executor
