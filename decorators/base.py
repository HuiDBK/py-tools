#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 通用装饰器模块 }
# @Date: 2022/11/26 16:16
import time
import asyncio
import threading
import functools
from typing import Type

from exceptions.base import MaxTimeoutException, MaxRetryException


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
        print(type(ret))
        use_time = time.time() - start_ts
        print(f"func {func.__name__} use {use_time}s")
        return ret

    return wrapper


def task_retry(
        max_retry_count: int = 5,
        time_interval: int = 2,
        max_timeout: int = None,
        catch_exc: Type[BaseException] = Exception
):
    """
    任务重试装饰器
    Args:
        max_retry_count: 最大重试次数 默认 5 次
        time_interval: 每次重试间隔 默认 2s
        max_timeout: 最大超时时间，单位s 默认为 None,
        catch_exc: 指定捕获的异常类用于特定的异常重试 默认捕获 Exception
    """

    def _task_retry(task_func):

        @functools.wraps(task_func)
        def sync_wrapper(*args, **kwargs):
            # 函数循环重试
            start_time = time.time()
            for retry_count in range(max_retry_count):
                print(f"execute count {retry_count + 1}")
                use_time = time.time() - start_time
                if max_timeout and use_time > max_timeout:
                    # 超出最大超时时间
                    raise MaxTimeoutException(f"execute timeout, use time {use_time}s, max timeout {max_timeout}")

                try:
                    task_ret = task_func(*args, **kwargs)
                    return task_ret
                except catch_exc as e:
                    print(f"fail {str(e)}")
                    time.sleep(time_interval)
            else:
                # 超过最大重试次数, 抛异常终止
                raise MaxRetryException(f"超过最大重试次数失败, max_retry_count {max_retry_count}")

        @functools.wraps(task_func)
        async def async_wrapper(*args, **kwargs):
            # 异步循环重试
            start_time = time.time()
            for retry_count in range(max_retry_count):
                print(f"execute count {retry_count + 1}")
                use_time = time.time() - start_time
                if max_timeout and use_time > max_timeout:
                    # 超出最大超时时间
                    raise MaxTimeoutException(f"execute timeout, use time {use_time}s, max timeout {max_timeout}")

                try:
                    return await task_func(*args, **kwargs)
                except catch_exc as e:
                    print(f"fail {str(e)}")
                    await asyncio.sleep(time_interval)
            else:
                # 超过最大重试次数, 抛异常终止
                raise MaxRetryException(f"超过最大重试次数失败, max_retry_count {max_retry_count}")

        # 异步函数判断
        wrapper_func = async_wrapper if asyncio.iscoroutinefunction(task_func) else sync_wrapper
        return wrapper_func

    return _task_retry
