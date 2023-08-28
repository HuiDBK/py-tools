#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 单例元类测试 }
# @Date: 2023/08/28 11:01
import threading

from py_tools.meta_cls import SingletonMetaCls


class TestSingletonMetaCls:
    """ 单例元类测试 """
    singleton_set = set()

    class Foo(metaclass=SingletonMetaCls):

        def bar(self):
            pass

    def create_singleton(self):
        self.singleton_set.add(id(self.Foo()))

    def test_singleton_meta_cls(self):
        assert self.Foo() is self.Foo()

        # 多线程测试单例
        thread_list = list()
        for i in range(10):
            t = threading.Thread(target=self.create_singleton)
            t.start()
            thread_list.append(t)

        for thread in thread_list:
            thread.join()

        # 判断单例集合中只有一个对象说明地址全部一样
        assert len(self.singleton_set) == 1
