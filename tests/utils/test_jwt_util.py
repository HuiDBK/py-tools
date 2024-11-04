#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: test_jwt_util.py
# @Desc: { test jwt util }
# @Date: 2024/11/04 15:32
import datetime
import time

import pytest

from py_tools.utils import JWTUtil

# 设置测试用的密钥和算法
SECRET_KEY = "test_secret_key"
ALGORITHM = "HS256"


class TestJWTUtil:
    """JWTUtil 工具类的测试用例。"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """初始化 JWTUtil 实例，用于每个测试方法。"""
        self.jwt_util = JWTUtil(secret_key=SECRET_KEY, algorithm=ALGORITHM, expiration_minutes=1)

    def test_generate_token(self):
        """测试生成 JWT 令牌。"""
        data = {"user_id": "12345", "role": "admin"}
        token = self.jwt_util.generate_token(data)
        assert isinstance(token, str), "生成的令牌应该是字符串"

    def test_verify_token(self):
        """测试验证有效的 JWT 令牌。"""
        data = {"user_id": "12345", "role": "admin"}
        token = self.jwt_util.generate_token(data)
        decoded_data = self.jwt_util.verify_token(token)
        assert decoded_data is not None, "验证后的数据不应为空"
        assert decoded_data["user_id"] == "12345", "解码数据中的 user_id 应该与输入数据匹配"
        assert decoded_data["role"] == "admin", "解码数据中的 role 应该与输入数据匹配"

    def test_verify_token_expired(self):
        """测试过期的 JWT 令牌验证。"""
        data = {"user_id": "12345", "role": "admin"}
        token = self.jwt_util.generate_token(data, expires_delta=datetime.timedelta(seconds=1))

        # 等待令牌过期
        time.sleep(2)
        decoded_data = self.jwt_util.verify_token(token)
        assert decoded_data is None, "过期的令牌应返回 None"

    def test_refresh_token(self):
        """测试刷新 JWT 令牌。"""
        data = {"user_id": "12345", "role": "admin"}
        token = self.jwt_util.generate_token(data, expires_delta=datetime.timedelta(seconds=5))

        # 在原令牌过期前刷新令牌
        refreshed_token = self.jwt_util.refresh_token(token, expires_delta=datetime.timedelta(minutes=1))
        assert refreshed_token is not None, "刷新后的令牌不应为空"
        assert refreshed_token != token, "刷新后的令牌应不同于原令牌"

        # 验证刷新后的令牌有效性
        decoded_data = self.jwt_util.verify_token(refreshed_token)
        assert decoded_data is not None, "刷新后的令牌验证应成功"
        assert decoded_data["user_id"] == "12345", "刷新令牌的解码数据应与原数据相同"
        assert decoded_data["role"] == "admin", "刷新令牌的解码数据应与原数据相同"
