#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: test_chatbot.py
# @Desc: { webhook机器人单测 }
# @Date: 2024/08/08 10:11
from unittest.mock import MagicMock, patch

import pytest

from py_tools.chatbot import (
    ChatBotFactory,
    ChatBotType,
    DingTalkChatBot,
    FeiShuAppServer,
    FeiShuChatBot,
    FeiShuTaskChatBot,
    WeComChatbot,
)
from py_tools.enums.feishu import FeishuReceiveType
from py_tools.exceptions import SendMsgException


class TestChatBot:
    feishu_bot = FeiShuChatBot(webhook_url="test_url", secret="test_secret")
    dingtalk_bot = DingTalkChatBot(webhook_url="test_url", secret="test_secret")
    wecom_bot = WeComChatbot(webhook_url="test_url", secret="test_secret")

    @classmethod
    def chatbots(cls):
        return [cls.feishu_bot, cls.dingtalk_bot, cls.wecom_bot]

    def test_get_sign(self):
        timestamp = "1609459200"
        secret = "test_secret"
        for bot in self.chatbots():
            assert bot._get_sign(timestamp, secret) == bot._get_sign(timestamp, secret)

    @pytest.fixture
    def mock_request_post(self, mocker):
        return mocker.patch("requests.post")

    def get_bot_mock_post_data(self, mock_request_post, bot):
        code_key = ""
        if isinstance(bot, FeiShuChatBot):
            code_key = "code"
            mock_request_post.return_value.json.return_value = {code_key: 0, "message": "ok"}
        elif isinstance(bot, DingTalkChatBot):
            code_key = "errcode"
            mock_request_post.return_value.json.return_value = {code_key: 0, "message": "ok"}
        elif isinstance(bot, WeComChatbot):
            code_key = MagicMock()
            code_key.status_code = 200
            mock_request_post.return_value = code_key

        return code_key

    def test_send_msg(self, mock_request_post):
        for bot in self.chatbots():
            code_key = self.get_bot_mock_post_data(mock_request_post, bot)
            ret = bot.send_msg("test message")
            if isinstance(ret, dict):
                assert ret.get(code_key) == 0
            else:
                assert ret.status_code == 200

    def test_send_msg_failure(self, mock_request_post):
        mock_request_post.return_value.json.return_value = {"code": 1, "message": "error"}
        with pytest.raises(SendMsgException):
            for bot in self.chatbots():
                bot.send_msg("test message")


class TestChatBotFactory(TestChatBot):
    def test_bot_factory_send_msg(self, mock_request_post):
        mock_request_post.return_value.json.return_value = {"code": 0, "message": "ok"}
        bot = ChatBotFactory(chatbot_type=ChatBotType.FEISHU_CHATBOT).build(
            webhook_url="test_url", secret="test_secret"
        )
        bot.send_msg("test message")

        mock_request_post.return_value.json.return_value = {"code": -1, "message": "ok"}
        with pytest.raises(SendMsgException):
            bot.send_msg("test message")


class TestFeiShuAppServer:
    @pytest.fixture
    def app_server(self):
        return FeiShuAppServer(app_id="test_app_id", app_secret="test_app_secret")

    @pytest.fixture
    def mock_tenant_access_token(self, mocker):
        mock_post = mocker.patch("requests.post")
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 0, "tenant_access_token": "mock_token", "expire": 3600}
        mock_post.return_value = mock_response
        return mock_post

    @patch("requests.post")
    def test_get_tenant_access_token(self, mock_post, app_server):
        # Mock the response from requests
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 0, "tenant_access_token": "mock_token", "expire": 3600}
        mock_post.return_value = mock_response

        token = app_server._get_tenant_access_token()
        assert token == "mock_token"

    @patch("requests.post")
    def test_get_user_open_id(self, mock_post, app_server):
        # Mock the response from requests
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "code": 0,
            "data": {"user_list": [{"mobile": "130xxxx1752", "user_id": "ou_xxx"}]},
        }
        mock_post.return_value = mock_response

        user_list = app_server._get_user_open_id(mobiles=["130xxxx1752"])
        assert user_list == [{"mobile": "130xxxx1752", "user_id": "ou_xxx"}]

    @patch("requests.get")
    def test_get_user_or_bot_groups(self, mock_get, app_server, mock_tenant_access_token):
        # Mock the response from requests
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "code": 0,
            "data": {"items": [{"name": "test_group", "chat_id": "test_chat_id"}], "has_more": False},
        }
        mock_get.return_value = mock_response

        groups = app_server._get_user_or_bot_groups()
        assert groups == [{"name": "test_group", "chat_id": "test_chat_id"}]

    @patch("requests.post")
    def test_send_msg(self, mock_post, app_server):
        # Mock the response from requests
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 0}
        mock_post.return_value = mock_response

        app_server.send_msg("test message", FeishuReceiveType.OPEN_ID, "test_open_id")


class TestFeiShuTaskChatBot:
    @pytest.fixture
    def chat_bot(self):
        return FeiShuTaskChatBot(app_id="test_app_id", app_secret="test_app_secret")

    @patch("requests.post")
    def test_user_task_notify(self, mock_post, chat_bot):
        # Mock the response from requests
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "code": 0,
            "data": {"user_list": [{"mobile": "130xxxx1752", "user_id": "ou_xxx"}]},
        }
        mock_post.return_value = mock_response

        with patch.object(chat_bot, "send_msg") as mock_send_msg:
            chat_bot.user_task_notify("test content", receive_mobiles=["130xxxx1752"])
            mock_send_msg.assert_called_with(
                "test content", receive_id_type=FeishuReceiveType.OPEN_ID, receive_id="ou_xxx"
            )

    @patch("requests.get")
    @patch("requests.post")
    def test_user_group_task_notify(self, mock_post, mock_get, chat_bot):
        # Mock the response from requests
        mock_get_response = MagicMock()
        mock_get_response.json.return_value = {
            "code": 0,
            "data": {"items": [{"name": "test_group", "chat_id": "test_chat_id"}], "has_more": False},
        }
        mock_get.return_value = mock_get_response

        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {
            "code": 0,
            "data": {"user_list": [{"mobile": "130xxxx1752", "user_id": "ou_xxx"}]},
        }
        mock_post.return_value = mock_post_response

        with patch.object(chat_bot, "send_msg") as mock_send_msg:
            chat_bot.user_group_task_notify("test content", "test_group", receive_mobiles=["130xxxx1752"])
            mock_send_msg.assert_called()
