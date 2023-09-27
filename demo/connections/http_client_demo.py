#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/08/10 11:39
import asyncio

from py_tools.enums import RespFmt
from py_tools.logging import logger
from py_tools.connections.http import HttpClient, AsyncHttpClient


async def async_http_client_demo():
    logger.debug("async_http_client_demo")
    url = "http://www.baidu.com"

    # 调用
    data = await AsyncHttpClient().get(url, resp_fmt=RespFmt.TEXT)
    logger.debug(data)


def sync_http_client_demo():
    logger.debug("sync_http_client_demo")
    url = "http://www.baidu.com"
    http_client = HttpClient()
    for i in range(2):
        text_content = http_client.get(url).text
        logger.debug(text_content)


async def main():
    await asyncio.gather(*[async_http_client_demo(), async_http_client_demo()])
    # await async_http_client_demo()

    sync_http_client_demo()


if __name__ == '__main__':
    asyncio.run(main())
