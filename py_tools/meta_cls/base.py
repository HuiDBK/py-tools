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

    def _init_instance(cls, *args, **kwargs):
        if cls._instance:
            # 存在实例对象直接返回，减少锁竞争，提高性能
            return cls._instance

        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

    def __call__(cls, *args, **kwargs):
        instance = cls._init_instance(*args, **kwargs)
        reinit = kwargs.get("reinit", False)
        if reinit:
            # 重新初始化单例对象属性
            instance.__init__(*args, **kwargs)
        return instance
