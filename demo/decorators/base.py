#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/02/12 22:15
import asyncio
import time

from decorators.base import task_retry
from exceptions.base import MaxRetryException, MaxTimeoutException


@task_retry(max_retry_count=3, time_interval=1, catch_exc=ZeroDivisionError)
def user_place_order():
    # a = 1 / 0
    a = []
    b = a[0]
    print("user place order success")
    return {"code": 0, "msg": "ok"}


@task_retry(max_retry_count=5, time_interval=2, max_timeout=5)
async def user_place_order_async():
    """异步函数重试案例"""
    a = 1 / 0
    print("user place order success")
    return {"code": 0, "msg": "ok"}


async def io_test():
    """模拟io阻塞"""
    print("io test start")
    time.sleep(3)
    print("io test end")
    return "io test end"


async def main():
    # 同步案例
    try:
        ret = user_place_order()
        print(f"user place order ret {ret}")
    except MaxRetryException as e:
        # 超过最大重试次数处理
        print("MaxRetryException", e)
    except MaxTimeoutException as e:
        # 超过最大超时处理
        print("MaxTimeoutException", e)

    # 异步案例
    # ret = await user_place_order_async()
    # print(f"user place order ret {ret}")

    # 并发异步
    # order_ret, io_ret = await asyncio.gather(
    #     user_place_order_async(),
    #     io_test(),
    # )
    # print(f"io ret {io_ret}")
    # print(f"user place order ret {order_ret}")


if __name__ == '__main__':
    asyncio.run(main())
