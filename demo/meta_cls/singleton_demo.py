#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 元类demo模块 }
# @Date: 2023/08/28 11:18
from py_tools.meta_cls import SingletonMetaCls


class Foo(metaclass=SingletonMetaCls):

    def __init__(self):
        print("Foo __init__")
        self.bar = "bar"

    def __new__(cls, *args, **kwargs):
        print("Foo __new__")
        return super().__new__(cls, *args, **kwargs)

    def tow_bar(self):
        return self.bar * 2


foo1 = Foo()
foo2 = Foo()
print("foo1 is foo2", foo1 is foo2)
print("foo2 two_bar", foo2.tow_bar())


class Demo(Foo):

    def __init__(self):
        self.bar = "demo_bar"


demo1 = Demo()
demo2 = Demo()
print("demo1 is demo2", demo1 is demo2)
print("demo2 two_bar", demo2.tow_bar())
