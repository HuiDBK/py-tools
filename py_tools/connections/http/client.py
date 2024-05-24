#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { http客户端 }
# @Date: 2023/08/10 09:33
import aiohttp
from datetime import timedelta

import requests
from aiohttp import ClientResponse

from py_tools.enums import HttpMethod


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
            **self.kwargs
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
        >>>
        >>> async for chunk in AsyncHttpClient().get(url).stream(chunk_size=512):
        >>>     # 流式调用
        >>>     print(chunk)

    Attributes:
        default_timeout: 默认请求超时时间,单位秒
        default_headers: 默认请求头字典
        new_session: 是否使用的新的客户端，默认共享一个 ClientSession
    """
    # aiohttp 异步客户端
    client_session: aiohttp.ClientSession = None
    client_session_set = set()

    def __init__(self, timeout=timedelta(seconds=10), headers: dict = None, new_session=False, **kwargs):
        """构造异步HTTP客户端"""
        self.default_timeout = aiohttp.ClientTimeout(timeout.total_seconds())
        self.default_headers = headers or {}
        self.new_session = new_session
        self.kwargs = kwargs

    async def _get_client_session(self):
        if self.new_session:
            client_session = aiohttp.ClientSession(
                headers=self.default_headers, timeout=self.default_timeout, **self.kwargs
            )
            self.client_session_set.add(client_session)
            return client_session

        if self.client_session is not None:
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

    async def _request(
            self,
            method: HttpMethod,
            url: str,
            params: dict = None,
            data: dict = None,
            timeout: timedelta = None,
            headers: dict = None,
            **kwargs
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
        headers = self.default_headers.update(**headers)
        client_session = await self._get_client_session()
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

    async def post(self, url: str, data: dict = None, timeout: timedelta = None, **kwargs) -> AsyncRequest:
        """POST请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒

        Returns: AsyncRequest
        """
        return AsyncRequest(self, HttpMethod.GET, url, data=data, timeout=timeout, **kwargs)

    async def put(self, url: str, data: dict = None, timeout: timedelta = None, **kwargs):
        """PUT请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒

        Returns: AsyncRequest
        """
        return AsyncRequest(self, HttpMethod.GET, url, data=data, timeout=timeout, **kwargs)

    async def delete(self, url: str, data: dict = None, timeout: timedelta = None, **kwargs):
        """DELETE请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒

        Returns: AsyncRequest
        """
        return AsyncRequest(self, HttpMethod.GET, url, data=data, timeout=timeout, **kwargs)


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
            self,
            method: HttpMethod, url: str,
            params: dict = None, data: dict = None,
            timeout: timedelta = None, **kwargs
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
            **kwargs
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

    async def put(self, url: str, data: dict = None, timeout: timedelta = None, **kwargs):
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

    async def delete(self, url: str, data: dict = None, timeout: timedelta = None, **kwargs):
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
