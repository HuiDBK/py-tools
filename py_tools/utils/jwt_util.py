#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: jwt_util.py
# @Desc: { jwt 工具模块 }
# @Date: 2024/11/04 15:05
import datetime
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from loguru import logger


class JWTUtil:
    """JWT 工具类，用于生成和验证 JWT 令牌。

    Attributes:
        secret_key (str): 用于签名 JWT 的密钥。
        algorithm (str): 使用的加密算法，默认是 HS256。
        expiration_minutes (int): 令牌的默认过期时间，以分钟为单位。
    """

    def __init__(self, secret_key: str, algorithm: str = "HS256", expiration_minutes: int = 60 * 2):
        """初始化 JWTUtil 实例。

        Args:
            secret_key (str): 用于签名 JWT 的密钥。
            algorithm (str): 使用的加密算法，默认为 'HS256'。
            expiration_minutes (int): 令牌的默认过期时间（分钟）。
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration_minutes = expiration_minutes

    def generate_token(self, data: Dict[str, Any], expires_delta: Optional[datetime.timedelta] = None) -> str:
        """生成 JWT 令牌。

        Args:
            data (Dict[str, Any]): 令牌中包含的数据 (payload)。
            expires_delta (Optional[datetime.timedelta], optional): 自定义的过期时间。如果没有指定，则使用默认的过期时间。

        Returns:
            str: 生成的 JWT 字符串。
        """
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() + (expires_delta or datetime.timedelta(minutes=self.expiration_minutes))
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """验证 JWT 令牌并返回其中的数据。

        Args:
            token (str): 要验证的 JWT 字符串。

        Returns:
            Optional[Dict[str, Any]]: 如果验证成功，返回解码后的数据；如果验证失败，返回 None。
        """
        try:
            decoded_data = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return decoded_data
        except JWTError as e:
            logger.error(f"Token verification failed, {e}")
            return None

    def refresh_token(self, token: str, expires_delta: Optional[datetime.timedelta] = None) -> Optional[str]:
        """刷新 JWT 令牌。

        Args:
            token (str): 旧的 JWT 字符串。
            expires_delta (Optional[datetime.timedelta], optional): 自定义的过期时间。如果没有指定，则使用默认过期时间。

        Returns:
            Optional[str]: 新生成的 JWT 字符串；如果旧的令牌无效或已过期，返回 None。
        """
        decoded_data = self.verify_token(token)
        if not decoded_data:
            return None
        decoded_data.pop("exp", None)
        return self.generate_token(decoded_data, expires_delta)
