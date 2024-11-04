#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: jwt_util_demo.py
# @Desc: { jwt util demo }
# @Date: 2024/11/04 15:20
from datetime import timedelta

from loguru import logger

from py_tools.utils import JWTUtil


def main():
    # 初始化密钥和算法
    jwt_util = JWTUtil(secret_key="your_secret_key", algorithm="HS256")

    # 生成 JWT
    data = {"user_id": "12345", "role": "admin"}
    token = jwt_util.generate_token(data)
    logger.info(f"Generated Token: {token}")

    # 验证 JWT
    decoded_data = jwt_util.verify_token(token)
    if decoded_data:
        logger.info(f"Decoded Data: {decoded_data}")
    else:
        logger.info("Token is invalid or expired.")

    # 刷新 JWT
    refreshed_token = jwt_util.refresh_token(token, expires_delta=timedelta(days=1))
    logger.info(f"Refreshed Token: {refreshed_token}")


if __name__ == "__main__":
    main()
