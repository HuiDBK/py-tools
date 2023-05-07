#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { webhook机器人模块 }
# @Date: 2023/02/19 19:48
import hmac
import base64
import hashlib
import time
from urllib.parse import quote_plus

import requests

from py_tools.exceptions.base import SendMsgException


class BaseChatBot(object):
    """群聊机器人基类"""

    def __init__(self, webhook_url: str, secret: str = None):
        """
        初始化机器人
        Args:
            webhook_url: 机器人webhook地址
            secret: 安全密钥
        """
        self.webhook_url = webhook_url
        self.secret = secret

    def _get_sign(self, timestamp: str, secret: str):
        """
        获取签名(NotImplemented)
        Args:
            timestamp: 签名时使用的时间戳
            secret: 签名时使用的密钥

        Returns:
        """
        raise NotImplementedError

    def send_msg(self, content: str, timeout=10):
        """
        发送消息(NotImplemented)
        Args:
            content: 消息内容
            timeout: 发送消息请求超时时间 默认10秒

        Returns:
        """
        raise NotImplementedError


class FeiShuChatBot(BaseChatBot):
    """飞书机器人"""

    def _get_sign(self, timestamp: str, secret: str) -> str:
        """
        获取签名
        把 timestamp + "\n" + 密钥 当做签名字符串，使用 HmacSHA256 算法计算签名，再进行 Base64 编码
        Args:
            timestamp: 签名时使用的时间戳
            secret: 签名时使用的密钥

        Returns: sign
        """
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

        # 对结果进行base64处理
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign

    def send_msg(self, content: str, timeout=10):
        """
        发送消息
        Args:
            content: 消息内容
            timeout: 发送消息请求超时时间 默认10秒

        Raises:
            SendMsgException

        Returns:
        """
        msg_data = {
            "msg_type": "text",
            "content": {
                "text": f"{content}"
            }
        }
        if self.secret:
            timestamp = str(round(time.time()))
            sign = self._get_sign(timestamp=timestamp, secret=self.secret)
            msg_data["timestamp"] = timestamp
            msg_data["sign"] = sign

        try:
            resp = requests.post(url=self.webhook_url, json=msg_data, timeout=timeout)
            resp_info = resp.json()
            if resp_info.get("code") != 0:
                raise SendMsgException(f"FeiShuRobot send msg error, {resp_info}")
        except Exception as e:
            raise SendMsgException(f"FeiShuRobot send msg error {e}") from e


class DingTalkChatBot(BaseChatBot):
    """钉钉机器人"""

    def _get_sign(self, timestamp: str, secret: str):
        """
        获取签名
        把 timestamp + "\n" + 密钥当做签名字符串，使用 HmacSHA256 算法计算签名，
        然后进行 Base64 encode，最后再把签名参数再进行 urlEncode，得到最终的签名（需要使用UTF-8字符集）
        Args:
            timestamp: 签名时使用的时间戳
            secret: 签名时使用的密钥

        Returns: sign
        """
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = quote_plus(base64.b64encode(hmac_code))

        return sign

    def send_msg(self, content: str, timeout=10):
        """
        发送消息
        Args:
            content: 消息内容
            timeout: 发送消息请求超时时间 默认10秒

        Raises:
            SendMsgException

        Returns:
        """
        timestamp = str(round(time.time() * 1000))
        sign = self._get_sign(timestamp=timestamp, secret=self.secret)

        params = {
            "timestamp": timestamp,
            "sign": sign
        }
        msg_data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        try:
            resp = requests.post(url=self.webhook_url, json=msg_data, params=params, timeout=timeout)
            resp_info = resp.json()
            if resp_info.get("errcode") != 0:
                raise SendMsgException(f"DingTalkRobot send msg error, {resp_info}")
        except Exception as e:
            raise SendMsgException(f"DingTalkRobot send msg error {e}") from e


class WeComChatbot(BaseChatBot):
    """企业微信机器人"""

    def _get_sign(self, timestamp: str, secret: str):
        pass

    def send_msg(self, content: str, timeout=10):
        msg_data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        resp = requests.post(self.webhook_url, json=msg_data)
        if resp.status_code != 200:
            raise ValueError("Failed to send message")
