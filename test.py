#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 测试模块 }
# @Date: 2022/08/13 17:21
import asyncio
import time

from decorator import singleton, calc_time
from meta_cls import SingletonMetaCls


# @singleton
class Foo(object, metaclass=SingletonMetaCls):

    def __init__(self):
        self.foo = "foo"

    def foo_double(self):
        self.foo *= 2


@calc_time
async def single_test():
    time.sleep(1)
    f = Foo()
    f.foo_double()
    print(f.foo)
    return "hui"


async def main():
    ret = await single_test()
    print(ret)


if __name__ == '__main__':
    asyncio.run(main())
