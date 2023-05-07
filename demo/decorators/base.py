#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/02/12 22:15
import asyncio
import time

from loguru import logger

from py_tools.decorators import retry, set_timeout
from py_tools.exceptions import MaxRetryException, MaxTimeoutException


@retry()
def user_place_order_success_demo():
    """用户下单成功模拟"""
    logger.debug("user place order success")
    return {"code": 0, "msg": "ok"}


@retry(max_count=3, interval=3)
def user_place_order_fail_demo():
    """用户下单失败模拟"""
    a = 1 / 0  # 使用除零异常模拟业务错误
    logger.debug("user place order success")
    return {"code": 0, "msg": "ok"}


@set_timeout(2)
@retry(max_count=3)
def user_place_order_timeout_demo():
    """用户下单失败模拟"""
    time.sleep(5)  # 模拟业务超时
    logger.debug("user place order success")
    return {"code": 0, "msg": "ok"}


@retry(max_count=2, interval=3)
async def async_user_place_order_demo():
    logger.debug("user place order success")
    return {"code": 0, "msg": "ok"}


@retry(max_count=2)
async def async_user_place_order_fail_demo():
    a = 1 / 0
    logger.debug("user place order success")
    return {"code": 0, "msg": "ok"}


@set_timeout(2)
@retry(max_count=3)
async def async_user_place_order_timeout_demo():
    await asyncio.sleep(3)
    logger.debug("user place order success")
    return {"code": 0, "msg": "ok"}


def sync_demo():
    """同步案例"""
    user_place_order_success_demo()

    try:
        user_place_order_fail_demo()
    except MaxRetryException as e:
        # 超出最大重新次数异常，业务逻辑处理
        logger.debug(f"sync 超出最大重新次数 {e}")

    try:
        user_place_order_timeout_demo()
    except MaxTimeoutException as e:
        # 超时异常，业务逻辑处理
        logger.debug(f"sync 超时异常, {e}")


async def async_demo():
    """异步案例"""
    await async_user_place_order_demo()

    try:
        await async_user_place_order_fail_demo()
    except MaxRetryException as e:
        logger.debug(f"async 超出最大重新次数 {e}")

    try:
        await async_user_place_order_timeout_demo()
    except MaxTimeoutException as e:
        logger.debug(f"async 超时异常, {e}")


async def main():
    # sync_demo()

    await async_demo()


if __name__ == '__main__':
    asyncio.run(main())
