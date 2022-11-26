#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 元类模块 }
# @Date: 2022/11/26 16:43
import threading


class SingletonMetaCls(type):
    """ 单例元类 """
    _instance_lock = threading.Lock()

    def __init__(cls, *args, **kwargs):
        cls._instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls._instance:
            # 存在实例对象直接返回，避免锁竞争，提高性能
            return cls._instance

        with cls._instance_lock:
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
