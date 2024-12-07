#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { http客户端 }
# @Date: 2023/08/10 09:33
from datetime import timedelta
from pathlib import Path
from typing import Any, Union

import aiohttp
import requests
from aiohttp import ClientResponse

from py_tools.enums.http import HttpMethod
from py_tools.utils.file_util import FileUtil


class AsyncRequest:
    def __init__(self, client, method: HttpMethod, url, **kwargs):
        self.client = client
        self.method = method
        self.url = url
        self.params = kwargs.pop("params", None)
        self.data = kwargs.pop("data", None)
        self.timeout = kwargs.pop("timeout", None)
        self.headers = kwargs.pop("headers", None)
        self.kwargs = kwargs

    async def execute(self) -> ClientResponse:
        return await self.client._request(
            self.method,
            self.url,
            params=self.params,
            data=self.data,
            timeout=self.timeout,
            headers=self.headers,
            **self.kwargs,
        )

    async def json(self):
        async with await self.execute() as response:
            return await response.json()

    async def text(self):
        async with await self.execute() as response:
            return await response.text()

    async def bytes(self):
        async with await self.execute() as response:
            return await response.read()

    async def stream(self, chunk_size=1024):
        async with await self.execute() as response:
            async for chunk in response.content.iter_chunked(chunk_size):
                yield chunk


class AsyncHttpClient:
    """异步HTTP客户端(支持链式调用)

    基于aiohttp封装，实现了常见的HTTP方法,支持设置超时时间、请求参数等，简化了异步调用的层级缩进。

    Examples:
        >>> url = "https://juejin.cn/"
        >>> resp = await AsyncHttpClient().get(url).execute()
        >>> text_data = await AsyncHttpClient().get(url, params={"test": "hui"}).text()
        >>> json_data = await AsyncHttpClient().post(url, data={"test": "hui"}).json()
        >>> byte_data = await AsyncHttpClient().get(url).bytes()
        >>> upload_file_ret = await AsyncHttpClient().upload_file(url, file="test.txt").json()
        >>>
        >>> async for chunk in AsyncHttpClient().get(url).stream(chunk_size=512):
        >>>     # 流式调用
        >>>     print(chunk)

    Attributes:
        default_timeout: 默认请求超时时间,单位秒
        default_headers: 默认请求头字典
        new_session: 是否使用的新的客户端，默认共享一个 ClientSession
    """

    # aiohttp 异步客户端(全局共享)
    client_session: aiohttp.ClientSession = None
    client_session_set = set()

    def __init__(self, timeout=timedelta(seconds=10), headers: dict = None, new_session=False, **kwargs):
        """构造异步HTTP客户端"""
        self.default_timeout = aiohttp.ClientTimeout(timeout.total_seconds())
        self.default_headers = headers or {}
        self.new_session = new_session
        self.cur_session: aiohttp.ClientSession = None
        self.kwargs = kwargs

    async def __aenter__(self):
        self.new_session = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._close_cur_session()

    async def _close_cur_session(self):
        if self.cur_session:
            await self.cur_session.close()
            if self.cur_session == AsyncHttpClient.client_session:
                AsyncHttpClient.client_session = None

        if self.cur_session in self.client_session_set:
            self.client_session_set.remove(self.cur_session)

    async def _get_client_session(self):
        if self.new_session:
            client_session = aiohttp.ClientSession(
                headers=self.default_headers, timeout=self.default_timeout, **self.kwargs
            )
            self.client_session_set.add(client_session)
            return client_session

        if self.client_session is not None and not self.client_session.closed:
            return self.client_session

        AsyncHttpClient.client_session = aiohttp.ClientSession(
            headers=self.default_headers, timeout=self.default_timeout, **self.kwargs
        )
        self.client_session_set.add(AsyncHttpClient.client_session)
        return self.client_session

    @classmethod
    async def close(cls):
        for client_session in cls.client_session_set:
            await client_session.close()

        cls.client_session_set.clear()
        cls.client_session = None

    async def _request(
        self,
        method: HttpMethod,
        url: str,
        params: dict = None,
        data: dict = None,
        timeout: timedelta = None,
        headers: dict = None,
        **kwargs,
    ):
        """内部请求实现方法

        创建客户端会话,构造并发送HTTP请求,返回响应对象

        Args:
            method: HttpMethod 请求方法, 'GET', 'POST' 等
            url: 请求URL
            params: 请求查询字符串参数字典
            data: 请求体数据字典
            timeout: 超时时间,单位秒
            headers: 请求头
            kwargs: 其他关键字参数

        Returns:
            httpx.Response: HTTP响应对象
        """
        timeout = timeout or self.default_timeout
        if isinstance(timeout, timedelta):
            timeout = aiohttp.ClientTimeout(timeout.total_seconds())

        headers = headers or {}
        headers.update(self.default_headers)
        client_session = await self._get_client_session()
        self.cur_session = client_session
        return await client_session.request(
            method.value, url, params=params, data=data, timeout=timeout, headers=headers, **kwargs
        )

    def get(self, url: str, params: dict = None, timeout: timedelta = None, **kwargs) -> AsyncRequest:
        """GET请求

        Args:
            url: 请求URL
            params: 请求查询字符串参数字典
            timeout: 请求超时时间,单位秒

        Returns: AsyncRequest
        """

        return AsyncRequest(self, HttpMethod.GET, url, params=params, timeout=timeout, **kwargs)

    def post(self, url: str, data: Union[dict, Any] = None, timeout: timedelta = None, **kwargs) -> AsyncRequest:
        """POST请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒

        Returns: AsyncRequest
        """
        return AsyncRequest(self, HttpMethod.POST, url, data=data, timeout=timeout, **kwargs)

    def put(self, url: str, data: Union[dict, Any], timeout: timedelta = None, **kwargs):
        """PUT请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒

        Returns: AsyncRequest
        """
        return AsyncRequest(self, HttpMethod.PUT, url, data=data, timeout=timeout, **kwargs)

    def delete(self, url: str, data: Union[dict, Any], timeout: timedelta = None, **kwargs):
        """DELETE请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒

        Returns: AsyncRequest
        """
        return AsyncRequest(self, HttpMethod.DELETE, url, data=data, timeout=timeout, **kwargs)

    def upload_file(
        self,
        url: str,
        file: Union[str, bytes, Path],
        file_field: str = "file",
        filename: str = None,
        method=HttpMethod.POST,
        timeout: timedelta = None,
        content_type: str = None,
        **kwargs,
    ) -> AsyncRequest:
        """
        上传文件
        Args:
            url: 请求URL
            file: 文件路径 or 字节数据
            file_field: 文件参数字段 默认"file"
            filename: 文件名名称
            method: 请求方法，默认POST
            content_type: 内容类型
            timeout: 请求超时时间,单位秒

        Returns: AsyncRequest
        """
        form_data = aiohttp.FormData()
        _filename, file_bytes, mime_type = FileUtil.get_file_info(file, filename=filename)
        filename = filename or _filename
        content_type = content_type or mime_type
        form_data.add_field(name=file_field, value=file_bytes, filename=filename, content_type=content_type)
        return AsyncRequest(self, method, url, data=form_data, timeout=timeout, **kwargs)


class HttpClient:
    """同步HTTP客户端

    通过request封装，实现了常见的HTTP方法,支持设置超时时间、请求参数等，链式调用

    Examples:
        >>> HttpClient().get("http://www.baidu.com").text
        >>> HttpClient().get("http://www.google.com", params={"name": "hui"}).bytes
        >>> HttpClient().post("http://www.google.com", data={"name": "hui"}).json

    Attributes:
        default_timeout: 默认请求超时时间,单位秒
        default_headers: 默认请求头字典
        client: request 客户端
        response: 每次实例请求的响应
    """

    def __init__(self, timeout=timedelta(seconds=10), headers: dict = None):
        """构造异步HTTP客户端"""
        self.default_timeout = timeout
        self.default_headers = headers or {}
        self.client = requests.session()
        self.response: requests.Response = None

    def _request(
        self, method: HttpMethod, url: str, params: dict = None, data: dict = None, timeout: timedelta = None, **kwargs
    ):
        """内部请求实现方法

        创建客户端会话,构造并发送HTTP请求,返回响应对象

        Args:
            method: HttpMethod 请求方法, 'GET', 'POST' 等
            url: 请求URL
            params: 请求查询字符串参数字典
            data: 请求体数据字典
            timeout: 超时时间,单位秒
            kwargs: 其他关键字参数

        Returns:
            httpx.Response: HTTP响应对象
        """
        timeout = timeout or self.default_timeout
        headers = self.default_headers or {}
        self.response = self.client.request(
            method=method.value,
            url=url,
            params=params,
            data=data,
            headers=headers,
            timeout=timeout.total_seconds(),
            **kwargs,
        )
        return self.response

    @property
    def json(self):
        return self.response.json()

    @property
    def bytes(self):
        return self.response.content

    @property
    def text(self):
        return self.response.text

    def get(self, url: str, params: dict = None, timeout: timedelta = None, **kwargs):
        """GET请求

        Args:
            url: 请求URL
            params: 请求查询字符串参数字典
            timeout: 请求超时时间,单位秒

        Returns:
            self 自身对象实例
        """

        self._request(HttpMethod.GET, url, params=params, timeout=timeout, **kwargs)
        return self

    def post(self, url: str, data: dict = None, timeout: timedelta = None, **kwargs):
        """POST请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒

        Returns:
            self 自身对象实例
        """
        self._request(HttpMethod.POST, url, data=data, timeout=timeout, **kwargs)
        return self

    def put(self, url: str, data: dict = None, timeout: timedelta = None, **kwargs):
        """PUT请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒

        Returns:
            self 自身对象实例
        """
        self._request(HttpMethod.PUT, url, data=data, timeout=timeout, **kwargs)
        return self

    def delete(self, url: str, data: dict = None, timeout: timedelta = None, **kwargs):
        """DELETE请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒

        Returns:
            self 自身对象实例
        """
        self._request(HttpMethod.DELETE, url, data=data, timeout=timeout, **kwargs)
        return self
