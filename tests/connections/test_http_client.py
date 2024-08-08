#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: test_http_client.py
# @Desc: { http客户端单测 }
# @Date: 2024/08/08 15:20
from unittest.mock import AsyncMock, MagicMock

import pytest

from py_tools.connections.http import AsyncHttpClient, HttpClient


class TestAsyncHttpClient:
    test_url = "http://example.com"

    text_func_ret = "test_response"
    bytes_func_ret = b"test_bytes"
    json_func_ret = {"key": "value"}

    @pytest.fixture
    def mock_request(self, mocker):
        mocker_request = mocker.patch.object(AsyncHttpClient, "_request")

        mock_response = AsyncMock()
        mock_response.__aenter__.return_value = mock_response
        mock_response.__aexit__.return_value = AsyncMock()

        mock_response.text.return_value = self.text_func_ret
        mock_response.json.return_value = self.json_func_ret
        mock_response.read.return_value = self.bytes_func_ret

        mocker_request.return_value = mock_response

        return mock_response

    @pytest.mark.asyncio
    async def test_get_text(self, mock_request):
        resp = await AsyncHttpClient().get(url=self.test_url).text()
        assert resp == self.text_func_ret

    @pytest.mark.asyncio
    async def test_post_put_json(self, mock_request):
        resp = await AsyncHttpClient().post(url=self.test_url, data={"method": "post"}).json()
        assert resp == self.json_func_ret

        resp = await AsyncHttpClient().put(url=self.test_url, data={"method": "put"}).json()
        assert resp == self.json_func_ret

    @pytest.mark.asyncio
    async def test_get_bytes(self, mock_request):
        resp = await AsyncHttpClient().get(url=self.test_url).bytes()
        assert resp == self.bytes_func_ret

    @pytest.mark.asyncio
    async def test_upload_file(self, mock_request):
        resp = await AsyncHttpClient().upload_file(url=self.test_url, file=__file__).json()
        assert resp == self.json_func_ret


class TestHttpClient:
    test_url = "http://example.com"

    text_func_ret = "test_response"
    bytes_func_ret = b"test_bytes"
    json_func_ret = {"key": "value"}

    @pytest.fixture
    def mock_request(self, mocker):
        mocker_request = mocker.patch("requests.Session.request")

        mock_response = MagicMock()
        mock_response.text = self.text_func_ret
        mock_response.json.return_value = self.json_func_ret
        mock_response.content = self.bytes_func_ret

        mocker_request.return_value = mock_response

        return mock_response

    def test_get_text(self, mock_request):
        resp = HttpClient().get(url=self.test_url).text
        assert resp == self.text_func_ret

    def test_post_put_json(self, mock_request):
        resp = HttpClient().post(url=self.test_url, data={"method": "post"}).json
        assert resp == self.json_func_ret

        resp = HttpClient().put(url=self.test_url, data={"method": "put"}).json
        assert resp == self.json_func_ret

    @pytest.mark.asyncio
    async def test_get_bytes(self, mock_request):
        resp = HttpClient().get(url=self.test_url).bytes
        assert resp == self.bytes_func_ret
