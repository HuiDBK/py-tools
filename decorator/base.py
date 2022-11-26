#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 通用装饰器模块 }
# @Date: 2022/11/26 16:16
import threading
import functools
import time


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
