#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { http客户端案例 }
# @Date: 2023/08/10 11:39
import asyncio

import aiohttp

from py_tools.connections.http import AsyncHttpClient, HttpClient
from py_tools.constants.const import BASE_DIR
from py_tools.logging import logger
from py_tools.utils.async_util import AsyncUtil


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
    logger.debug(f"text_data {text_data}")
    logger.debug(f"byte_data {byte_data}")

    # 上传文件
    form = aiohttp.FormData()
    file_path = BASE_DIR / "README.md"
    form.add_field("file", open(file_path, "rb"), filename="new_name.md", content_type="application/octet-stream")
    url = "http://localhost:8000/file_upload/file_params"
    upload_ret = await AsyncHttpClient().post(url=url, data=form).json()
    logger.debug(f"upload_ret {upload_ret}")

    # file_path
    upload_ret = await AsyncHttpClient().upload_file(url=url, file=file_path, filename="hui.md").json()
    logger.debug(f"upload_ret {upload_ret}")

    # file_bytes
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    upload_ret = await AsyncHttpClient().upload_file(url=url, file=file_bytes, filename="hui_bytes.md").json()
    logger.debug(f"upload_ret {upload_ret}")

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
    jobs = [async_http_client_demo(), async_http_client_demo()]
    # await asyncio.gather(*jobs)
    await AsyncUtil.run_jobs(jobs, show_progress=True)
    # await async_http_client_demo()

    # sync_http_client_demo()

    await AsyncHttpClient.close()


if __name__ == "__main__":
    asyncio.run(main())
