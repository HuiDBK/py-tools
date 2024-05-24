#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/08/10 11:39
import asyncio

from py_tools.logging import logger
from py_tools.connections.http import HttpClient, AsyncHttpClient


async def async_http_client_demo():
    logger.debug("async_http_client_demo")
    url = "https://juejin.cn/"

    # 调用
    resp = await AsyncHttpClient().get(url).execute()
    # json_data = await AsyncHttpClient().get(url).json()
    text_data = await AsyncHttpClient(new_session=True).get(url).text()
    byte_data = await AsyncHttpClient().get(url).bytes()

    logger.debug(f"resp {resp}")
    # logger.debug(f"json_data {json_data}")
    # logger.debug(f"text_data {text_data}")
    # logger.debug(f"byte_data {byte_data}")

    # 流式调用
    async for chunk in AsyncHttpClient().get(url).stream():
        print(chunk)


def sync_http_client_demo():
    logger.debug("sync_http_client_demo")
    url = "https://juejin.cn/"
    http_client = HttpClient()
    for i in range(2):
        text_content = http_client.get(url).text
        logger.debug(text_content)


async def main():
    await asyncio.gather(*[async_http_client_demo(), async_http_client_demo()])
    await async_http_client_demo()

    sync_http_client_demo()

    await AsyncHttpClient.close()


if __name__ == '__main__':
    asyncio.run(main())
